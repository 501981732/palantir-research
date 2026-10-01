import React, { useState } from 'react';
import { createRoot } from 'react-dom/client';
import { BaseForm } from '@osdk/react-components/action-form';
import { booleanField, textField } from './fixtures.js';
import './style.css';

function MockForm({ required }) {
  const [result, setResult] = useState(null);
  return <section className="probe-card">
    <p className="eyebrow">{required ? '01 · required boolean' : '02 · optional boolean'}</p>
    <h2>{required ? '必填布尔字段' : '非必填布尔字段'}</h2>
    <p className="description">默认值 False。点击 Submit，仅记录本地 mock 结果。</p>
    <BaseForm formContent={[textField(), booleanField(required)]}
      onSubmit={async (state) => { setResult(state); }} />
    <pre className="result">{result ? JSON.stringify(result, null, 2) : '尚未产生 mock 提交结果'}</pre>
  </section>;
}
function App() {
  return <main>
    <header><p className="eyebrow">LOCAL MOCK · PUBLIC NPM ARTIFACT</p><h1>OSDK / React 19 验证页</h1>
      <p>React 19.3.0 · @osdk/react-components 0.61.0 · OSDK peers 2.75.0</p>
      <p>真实 BaseForm 组件；普通字段；无 OsdkProvider、无 Foundry 数据、无 Action 执行。</p>
    </header>
    <div className="grid"><MockForm required={true}/><MockForm required={false}/></div>
  </main>;
}
createRoot(document.getElementById('root')).render(<App/>);
