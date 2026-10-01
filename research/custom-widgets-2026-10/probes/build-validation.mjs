// Published Vite plugin probes, not a Workshop host simulation. No network calls.
import { pathToFileURL } from 'node:url';
import { readFile, writeFile, mkdtemp, mkdir } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { createHash } from 'node:crypto';
const project = process.argv[2] ?? '/tmp/widget-build-research/probe/official-widget';
const plugin = path.join(project, 'node_modules/@osdk/widget.vite-plugin/build/esm');
const { validateWidgetConfig } = await import(pathToFileURL(path.join(plugin, 'common/validateWidgetConfig.js')));
const { buildWidgetSetManifest, convertParameters } = await import(pathToFileURL(path.join(plugin, 'build-plugin/buildWidgetSetManifest.js')));
const { extractBuildOutputs } = await import(pathToFileURL(path.join(plugin, 'build-plugin/extractBuildOutputs.js')));
const { autoVersion } = await import(pathToFileURL(path.join(project, 'node_modules/@osdk/foundry-config-json/build/esm/autoVersion.js')));
const baseline = () => ({ id: 'probeWidget', name: 'Probe', type: 'workshop', parameters: { count: { type: 'number', displayName: 'Count' } }, events: { updateCount: { displayName: 'Update', parameterUpdateIds: ['count'] } } });
const cases = [];
function check(name, fn, expected) {
  let result = 'accepted'; let error;
  try { fn(); } catch (e) { result = 'rejected'; error = e.message; }
  cases.push({name, expected, observed: result, pass: result === expected, ...(error ? {error} : {})});
}
check('valid baseline', () => validateWidgetConfig(baseline()), 'accepted');
check('widget id snake_case', () => validateWidgetConfig({...baseline(), id: 'bad_id'}), 'rejected');
check('parameter id snake_case', () => validateWidgetConfig({...baseline(), parameters: {bad_id: {type:'number',displayName:'Bad'}}}), 'rejected');
check('event id snake_case is not checked by plugin', () => validateWidgetConfig({...baseline(), events: {'bad_event': {displayName:'Bad', parameterUpdateIds:[]}}}), 'accepted');
check('51 parameters not checked by plugin', () => validateWidgetConfig({...baseline(), parameters: Object.fromEntries(Array.from({length:51}, (_, i) => ['param'+i, {type:'number',displayName:'P'}]))}), 'accepted');
check('51 events not checked by plugin', () => validateWidgetConfig({...baseline(), events: Object.fromEntries(Array.from({length:51}, (_, i) => ['event'+i, {displayName:'E',parameterUpdateIds:[]}]))}), 'accepted');
check('event references absent parameter not checked by plugin', () => validateWidgetConfig({...baseline(), events: {bad:{displayName:'E',parameterUpdateIds:['missing']}}}), 'accepted');
check('objectSet missing generated RID metadata', () => validateWidgetConfig({...baseline(), parameters: {objects:{type:'objectSet',displayName:'Objects',allowedType:{type:'object',apiName:'Todo'}}}}), 'rejected');
check('event updating readonly mapTileLayer', () => validateWidgetConfig({...baseline(), parameters: {count:{type:'mapTileLayer',displayName:'Map'}}}), 'rejected');
const build = c => ({widgetConfig:c,scripts:[{src:'/assets/probe.js',scriptType:'module'}],stylesheets:['/assets/probe.css']});
check('duplicate widget IDs in set', () => buildWidgetSetManifest('ri.widgetregistry..widget-set.probe','0.0.0',[build(baseline()),build(baseline())],{}), 'rejected');
const convertedObjectSets = Object.fromEntries(['object','interface'].map(type => [type, convertParameters({objects:{type:'objectSet',displayName:'Objects',allowedType:{type,apiName:'Sample',internalDoNotUseMetadata:{rid:'ri.ontology..'+type+'.probe'}}}}).objects]));
const htmlRoot = await mkdtemp(path.join(tmpdir(),'widget-html-probe-'));
for (const [name, html, expected] of [
  ['HTML external module script','<script type="module" src="/assets/a.js"></script>','accepted'],
  ['HTML inline script','<script>window.x=1</script>','rejected'],
  ['HTML script defer attribute','<script defer src="/assets/a.js"></script>','rejected'],
  ['HTML stylesheet media attribute','<link rel="stylesheet" media="print" href="/assets/a.css">','rejected']
]) {
  const f=path.join(htmlRoot,name.replaceAll(' ','-')+'.html');await writeFile(f,html);check(name,()=>extractBuildOutputs(f),expected);
}
const cwd=process.cwd();process.chdir(project);
const computedVersion=await autoVersion({type:'package-json'});process.chdir(cwd);
const manifest=JSON.parse(await readFile(path.join(project,'dist/.palantir/widgets.config.json'),'utf8'));
const lockRaw=await readFile(path.join(project,'package-lock.json'));
const lock=JSON.parse(lockRaw);const resolved={};
for(const name of ['@osdk/widget.vite-plugin','@osdk/widget.client','@osdk/widget.client-react','@osdk/widget.api','@osdk/foundry-config-json','react','react-dom','vite','typescript']) resolved[name]=lock.packages['node_modules/'+name].version;
const output={retrievedDate:'2026-10-01',scope:'Local published-plugin validation and official no-OSDK template build; no Workshop host, tenant, API calls or mock SDK.',node:process.version,resolvedVersions:resolved,lockSha256:createHash('sha256').update(lockRaw).digest('hex'),computedVersion,manifest,cases,convertedObjectSets,allPass:cases.every(c=>c.pass)};
const dest = path.resolve(import.meta.dirname,'../evidence/build-probe-results.json');await writeFile(dest,JSON.stringify(output,null,2)+'\n');
console.log(JSON.stringify({cases:cases.length,allPass:output.allPass,resolvedVersions:resolved,output:dest},null,2));
