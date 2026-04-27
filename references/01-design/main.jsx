// App shell — composes Sidebar + active tab

function App() {
  const [tab, setTab] = useState('collect');
  const [server, setServer] = useState('local');

  const Tab = {
    collect: CollectTab,
    script:  ScriptTab,
    upload:  UploadTab,
    trend:   TrendTab,
  }[tab];

  return (
    <div data-screen-label={tab} style={{
      width: '100vw', height: '100vh',
      background: T.bg, color: T.text,
      fontFamily: T.font,
      display: 'flex', overflow: 'hidden',
    }}>
      <Sidebar tab={tab} setTab={setTab} server={server} setServer={setServer} />
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', minWidth: 0, background: T.bg }}>
        <Tab />
      </div>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
