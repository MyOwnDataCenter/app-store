#!/usr/bin/env node
// Checks every app in the store: node scripts/validate.mjs [--warnings] [--strict] [--root DIR]
//
// An app is a folder with a docker-compose.yml and an omarchy-app.yml. Errors are things that stop an app
// from installing or showing up properly, and they fail the run. Warnings are things worth a look; they
// are counted, and listed with --warnings. --strict turns warnings into failures too.
import {existsSync, readFileSync, readdirSync, statSync} from 'node:fs'
import {dirname, join} from 'node:path'
import {fileURLToPath} from 'node:url'
import {parse} from 'yaml'

const rootFlag = process.argv.indexOf('--root')
const root = rootFlag > 0 ? process.argv[rootFlag + 1] : join(dirname(fileURLToPath(import.meta.url)), '..')
const showAll = process.argv.includes('--warnings')
const strict = process.argv.includes('--strict')
const onGitHub = process.env.GITHUB_ACTIONS === 'true'

// The categories the store uses today. A new one is allowed; it just gets a warning so it is a choice.
const CATEGORIES = new Set(['files', 'media', 'developer', 'networking', 'social', 'ai', 'automation', 'finance', 'gaming', 'photography', 'crypto'])

const errors = []
const warnings = new Map() // kind -> [message]
const error = (app, file, message) => errors.push({app, file, message})
const warn = (kind, app, message) => warnings.set(kind, [...(warnings.get(kind) ?? []), `${app}: ${message}`])

function load(app, file) {
	const path = join(root, app, file)
	if (!existsSync(path)) return error(app, file, `${file} is missing`)
	try {
		const doc = parse(readFileSync(path, 'utf8'))
		if (!doc || typeof doc !== 'object' || Array.isArray(doc)) return error(app, file, `${file} should be a set of settings, not ${Array.isArray(doc) ? 'a list' : 'empty'}`)
		return doc
	} catch (e) {
		return error(app, file, `${file} isn't valid YAML: ${String(e.message).split('\n')[0]}`)
	}
}

// "nginx", "nginx:latest" and "ghcr.io/x/y" are not pinned; "nginx:1.27" and "x@sha256:..." are.
function unpinned(image) {
	if (typeof image !== 'string' || image.includes('${') || image.includes('@sha256:')) return false
	const last = image.slice(image.lastIndexOf('/') + 1)
	const tag = last.includes(':') ? last.slice(last.indexOf(':') + 1) : ''
	return tag === '' || tag === 'latest'
}

const text = (v) => typeof v === 'string' && v.trim() !== ''
const apps = readdirSync(root)
	.filter((n) => !n.startsWith('.') && n !== 'node_modules' && statSync(join(root, n)).isDirectory())
	.filter((n) => existsSync(join(root, n, 'docker-compose.yml')) || existsSync(join(root, n, 'omarchy-app.yml')))
	.sort()
const names = new Map()

for (const app of apps) {
	const compose = load(app, 'docker-compose.yml')
	const listing = load(app, 'omarchy-app.yml')
	const services = compose && typeof compose.services === 'object' && compose.services ? compose.services : null
	if (compose && (!services || Object.keys(services).length === 0)) error(app, 'docker-compose.yml', 'has no services')

	if (listing) {
		const f = 'omarchy-app.yml'
		if (listing.manifestVersion !== 1) error(app, f, `manifestVersion should be 1, not ${JSON.stringify(listing.manifestVersion)}`)
		if (listing.id !== app) error(app, f, `id is ${JSON.stringify(listing.id)} but the folder is ${app}; they must match`)
		for (const key of ['name', 'tagline', 'description', 'category', 'icon']) if (!text(listing[key])) error(app, f, `${key} is missing`)
		if (!Number.isInteger(listing.port) || listing.port < 1 || listing.port > 65535) error(app, f, `port should be a number from 1 to 65535, not ${JSON.stringify(listing.port)}`)
		// path is optional: Omarchy Server opens the front page when it's left out.
		if (listing.path !== undefined && typeof listing.path !== 'string') error(app, f, `path should be text, not ${JSON.stringify(listing.path)}`)

		// An older-style app names its web port in an app_proxy service instead; Omarchy Server reads that too.
		if (listing.web === undefined && !(services && 'app_proxy' in services)) warn('no-web', app, 'has no web: block, so Omarchy Server cannot put its sign-in in front of the app')
		else if (listing.web === undefined) {
			// covered by app_proxy above
		} else if (!text(listing.web?.service) || !Number.isInteger(listing.web?.port)) error(app, f, 'web: needs a service name and a port number')
		else if (services && !(listing.web.service in services)) error(app, f, `web.service is ${JSON.stringify(listing.web.service)}, which is not a service in docker-compose.yml (${Object.keys(services).join(', ')})`)

		if (text(listing.category) && !CATEGORIES.has(listing.category)) warn('category', app, `category ${JSON.stringify(listing.category)} is not one the store uses yet`)
		if (text(listing.icon) && !/^https:\/\//.test(listing.icon)) warn('icon', app, `icon is not an https:// address: ${listing.icon}`)
		if (text(listing.name)) {
			const key = listing.name.trim().toLowerCase()
			names.set(key, [...(names.get(key) ?? []), app])
		}
	}

	if (services)
		for (const [service, def] of Object.entries(services)) {
			if (service === 'app_proxy') continue // a placeholder for the web port: it has no image of its own
			if (def?.image === undefined && def?.build === undefined && def?.extends === undefined) error(app, 'docker-compose.yml', `service ${service} has no image`)
			else if (unpinned(def.image)) warn('image', app, `${service} uses ${def.image}, which is not a fixed version`)
		}
}
for (const [name, list] of names) if (list.length > 1) warn('same-name', list.join(', '), `share the name ${JSON.stringify(name)}`)

for (const e of errors) console.log(onGitHub ? `::error file=${e.app}/${e.file}::${e.message}` : `error   ${e.app}/${e.file}: ${e.message}`)
const labels = {
	image: 'images that are not a fixed version',
	'no-web': 'listings without a web: block',
	category: 'listings in an unknown category',
	icon: 'icons that are not https://',
	'same-name': 'listings that share a name',
}
for (const [kind, list] of warnings) {
	console.log(`warning ${list.length} ${labels[kind] ?? kind}${showAll || list.length <= 3 ? '' : ` (--warnings lists them; first: ${list[0]})`}`)
	if (showAll || list.length <= 3) for (const w of list) console.log(`          ${w}`)
}
const count = [...warnings.values()].reduce((n, l) => n + l.length, 0)
console.log(`\n${apps.length} apps checked: ${errors.length} error${errors.length === 1 ? '' : 's'}, ${count} warning${count === 1 ? '' : 's'}`)
process.exit(errors.length || (strict && count) ? 1 : 0)
