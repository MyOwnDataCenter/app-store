// The store validator, run on small stores built in a temporary folder.
import assert from 'node:assert/strict'
import {spawnSync} from 'node:child_process'
import {mkdir, mkdtemp, rm, writeFile} from 'node:fs/promises'
import os from 'node:os'
import {dirname, join} from 'node:path'
import {after, test} from 'node:test'
import {fileURLToPath} from 'node:url'

const SCRIPT = join(dirname(fileURLToPath(import.meta.url)), 'validate.mjs')
const root = await mkdtemp(join(os.tmpdir(), 'store-'))
after(() => rm(root, {recursive: true, force: true}))

const LISTING = (id, extra = '') => `manifestVersion: 1
id: ${id}
name: "App ${id}"
tagline: "Does a thing"
icon: https://example.com/${id}.png
category: files
version: "1.0"
port: 3000
path: ""
web:
  service: web
  port: 80
description: >-
  Does a thing.
${extra}`
const COMPOSE = (image = 'nginx:1.27') => `services:\n  web:\n    image: ${image}\n    ports:\n      - "3000:80"\n`

let n = 0
// Builds a store from {folder: {compose, listing}} and runs the validator on it.
async function check(apps, flags = []) {
	const dir = join(root, `store${n++}`)
	await mkdir(dir)
	for (const [name, files] of Object.entries(apps)) {
		await mkdir(join(dir, name))
		if (files.compose !== undefined) await writeFile(join(dir, name, 'docker-compose.yml'), files.compose)
		if (files.listing !== undefined) await writeFile(join(dir, name, 'omarchy-app.yml'), files.listing)
	}
	const r = spawnSync('node', [SCRIPT, '--root', dir, ...flags], {encoding: 'utf8', env: {...process.env, GITHUB_ACTIONS: ''}})
	return {status: r.status, out: r.stdout + r.stderr}
}

test('a correct app passes, and a folder that is not an app is ignored', async () => {
	const r = await check({good: {compose: COMPOSE(), listing: LISTING('good')}, notes: {}})
	assert.equal(r.status, 0, r.out)
	assert.match(r.out, /1 apps checked: 0 errors, 0 warnings/)
})

test('each kind of mistake is an error that names the app and the file', async () => {
	const cases = [
		[{wrongid: {compose: COMPOSE(), listing: LISTING('other')}}, /error   wrongid\/omarchy-app\.yml: id is "other" but the folder is wrongid/],
		[{nolisting: {compose: COMPOSE()}}, /error   nolisting\/omarchy-app\.yml: omarchy-app\.yml is missing/],
		[{nocompose: {listing: LISTING('nocompose')}}, /error   nocompose\/docker-compose\.yml: docker-compose\.yml is missing/],
		[{badyaml: {compose: 'services: [unclosed', listing: LISTING('badyaml')}}, /error   badyaml\/docker-compose\.yml: docker-compose\.yml isn't valid YAML/],
		[{noservices: {compose: 'version: "3"\n', listing: LISTING('noservices')}}, /noservices\/docker-compose\.yml: has no services/],
		[{badweb: {compose: COMPOSE(), listing: LISTING('badweb').replace('service: web', 'service: nope')}}, /web\.service is "nope", which is not a service in docker-compose\.yml \(web\)/],
		[{badport: {compose: COMPOSE(), listing: LISTING('badport').replace('port: 3000', 'port: "x"')}}, /port should be a number from 1 to 65535, not "x"/],
		[{noname: {compose: COMPOSE(), listing: LISTING('noname').replace(/name: .*\n/, '')}}, /name is missing/],
		[{noimage: {compose: 'services:\n  web:\n    ports: ["1:1"]\n', listing: LISTING('noimage')}}, /service web has no image/],
	]
	for (const [apps, expected] of cases) {
		const r = await check(apps)
		assert.equal(r.status, 1, r.out)
		assert.match(r.out, expected)
	}
})

test('an app with an app_proxy service and no web: block is fine', async () => {
	const compose = `services:\n  app_proxy:\n    environment:\n      APP_HOST: x\n      APP_PORT: 80\n  web:\n    image: nginx:1.27\n`
	const listing = LISTING('proxied').replace(/web:\n  service: web\n  port: 80\n/, '')
	const r = await check({proxied: {compose, listing}})
	assert.equal(r.status, 0, r.out)
	assert.match(r.out, /0 errors, 0 warnings/)
})

test('an app with no web: block and no app_proxy warns that My Own Data Center cannot put sign-in in front', async () => {
	const listing = LISTING('noweb').replace(/web:\n  service: web\n  port: 80\n/, '')
	const r = await check({noweb: {compose: COMPOSE(), listing}})
	assert.equal(r.status, 0, r.out)
	assert.match(r.out, /has no web: block, so My Own Data Center cannot put its sign-in in front of the app/)
})

test('unfixed image versions are warnings: they do not fail, unless --strict', async () => {
	const apps = {a: {compose: COMPOSE('nginx:latest'), listing: LISTING('a')}, b: {compose: COMPOSE('nginx'), listing: LISTING('b')}, c: {compose: COMPOSE('ghcr.io/x/y:2.1'), listing: LISTING('c')}, d: {compose: COMPOSE('x/y@sha256:' + 'a'.repeat(64)), listing: LISTING('d')}, e: {compose: COMPOSE('${IMAGE:-x/y:1}'), listing: LISTING('e')}}
	const r = await check(apps)
	assert.equal(r.status, 0, r.out)
	assert.match(r.out, /warning 2 images that are not a fixed version/)
	assert.match(r.out, /a: web uses nginx:latest/)
	assert.match(r.out, /b: web uses nginx, which/)
	assert.equal((await check(apps, ['--strict'])).status, 1)
})

test('a registry with a port number is not mistaken for a tag', async () => {
	const r = await check({a: {compose: COMPOSE('registry.local:5000/team/app'), listing: LISTING('a')}, b: {compose: COMPOSE('registry.local:5000/team/app:3'), listing: LISTING('b')}})
	assert.match(r.out, /warning 1 images that are not a fixed version[\s\S]*a: web uses registry\.local:5000\/team\/app,/)
	assert.ok(!r.out.includes('b: web'))
})

test('two apps with the same name, an unknown category and a plain http icon are warnings', async () => {
	const r = await check({
		one: {compose: COMPOSE(), listing: LISTING('one').replace('"App one"', '"Same"').replace('category: files', 'category: weird')},
		two: {compose: COMPOSE(), listing: LISTING('two').replace('"App two"', '"same"').replace('https://example.com', 'http://example.com')},
	})
	assert.equal(r.status, 0, r.out)
	assert.match(r.out, /warning 1 listings in an unknown category[\s\S]*category "weird"/)
	assert.match(r.out, /warning 1 icons that are not https/)
	assert.match(r.out, /warning 1 listings that share a name[\s\S]*one, two: share the name "same"/)
})
