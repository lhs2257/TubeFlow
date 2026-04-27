// Tab 2: 대본 작성 — AI script generation

const SCRIPT_DRAFT = `[훅 — 0:00–0:08]
"여러분, 잠깐. 문어가 왼발잡이 오른발잡이가 있다는 사실, 알고 계셨나요?"
(클로즈업: 수족관 문어)

[인트로 — 0:08–0:25]
안녕하세요. 오늘은 무려 90%의 문어가 똑같은 다리를 먼저 사용한다는,
최근 학계를 뒤집은 연구를 가져왔습니다.
구독자분들 중에 동물 좋아하시는 분 — 끝까지 보시면 정말 재미있을 거예요.

[본론 1 — 핵심 사실 — 0:25–1:40]
2024년 미네소타 대학 해양생물학팀이 25마리의 거대 태평양 문어를 1년간 관찰한 결과,
무려 22마리가 먹이를 잡거나 도구를 사용할 때 "세 번째 오른쪽 다리"를 우선적으로 썼다고 합니다.

흥미로운 건 이게 단순한 습관이 아니라, 신경학적으로 한쪽 뇌엽이 더 발달했다는 거예요.
그러니까 우리가 오른손잡이인 것과 본질적으로 같다는 거죠.

[본론 2 — 왜 세 번째일까? — 1:40–2:30]
그럼 왜 하필 세 번째 다리일까요?
연구진의 가설은 — 시야 확보입니다…`;

function ScriptTab() {
  const [source, setSource] = useState('opt-2');
  const [tone, setTone] = useState('info');
  const [length, setLength] = useState('5min');
  const [hook, setHook] = useState('question');
  const [generating, setGenerating] = useState(false);
  const [script, setScript] = useState(SCRIPT_DRAFT);
  const [progress, setProgress] = useState(0);

  function generate() {
    setGenerating(true); setProgress(0);
    const id = setInterval(() => {
      setProgress(p => {
        if (p >= 100) { clearInterval(id); setGenerating(false); return 100; }
        return p + 4;
      });
    }, 70);
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <PageHeader
        title="대본 작성"
        subtitle="수집된 소재를 AI로 영상 대본으로 변환합니다"
        actions={
          <>
            <Button variant="ghost"     icon="folder" size="md">불러오기</Button>
            <Button variant="secondary" icon="check"  size="md">저장</Button>
          </>
        }
      />

      <div style={{ display: 'grid', gridTemplateColumns: '320px 1fr', flex: 1, minHeight: 0 }}>
        {/* Settings */}
        <div style={{ padding: '20px 24px', borderRight: `1px solid ${T.border}`, overflow: 'auto', display: 'flex', flexDirection: 'column', gap: 16 }}>
          <Field label="소재 선택">
            <Select value={source} onChange={e => setSource(e.target.value)}
              options={[
                { value: 'manual', label: '직접 입력...' },
                { value: 'opt-1', label: '20년 단골 할아버지의 마지막 자리' },
                { value: 'opt-2', label: 'TIL 문어는 왼발/오른발잡이가 있다' },
                { value: 'opt-3', label: '면접관이 우리 아빠였던 사연' },
              ]}
            />
          </Field>

          <div style={{
            background: T.panel2, border: `1px solid ${T.border}`,
            borderRadius: 8, padding: 12, fontSize: 12, color: T.textDim,
            lineHeight: 1.5,
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 6, color: T.textMute, fontSize: 10.5, fontWeight: 600, letterSpacing: '0.06em' }}>
              <Icon name="reddit" size={11} color="#FF7A45" />SOURCE PREVIEW
            </div>
            TIL 문어는 왼발잡이 오른발잡이가 있고, 90%는 세 번째 오른쪽 다리를 우선 사용한다
            <div style={{ marginTop: 8, display: 'flex', gap: 8, fontFamily: T.mono, fontSize: 10.5, color: T.textMute }}>
              <span>↑ 31.7k</span><span>💬 892</span><span>r/todayilearned</span>
            </div>
          </div>

          <div style={{ height: 1, background: T.border, margin: '4px 0' }} />

          <Field label="톤 / 스타일">
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 6 }}>
              {[
                { v: 'humor',   l: '🎭 유머',     d: '캐주얼한 농담' },
                { v: 'info',    l: '📊 정보',     d: '사실 중심'    },
                { v: 'story',   l: '📖 스토리',   d: '서사 중심'    },
                { v: 'shock',   l: '⚡ 충격',     d: '강한 훅'      },
              ].map(o => (
                <button key={o.v} onClick={() => setTone(o.v)} style={{
                  padding: '10px 10px', textAlign: 'left',
                  background: tone === o.v ? T.panel3 : T.panel2,
                  border: `1px solid ${tone === o.v ? T.accent : T.border}`,
                  borderRadius: 7, cursor: 'pointer',
                  display: 'flex', flexDirection: 'column', gap: 2,
                }}>
                  <span style={{ fontSize: 12, fontWeight: 600, color: T.text }}>{o.l}</span>
                  <span style={{ fontSize: 10.5, color: T.textMute }}>{o.d}</span>
                </button>
              ))}
            </div>
          </Field>

          <Field label="영상 길이">
            <SegmentedControl
              value={length} onChange={setLength}
              options={[
                { value: 'short', label: '쇼츠'  },
                { value: '3min',  label: '3분'   },
                { value: '5min',  label: '5분'   },
                { value: '10min', label: '10분+' },
              ]}
            />
          </Field>

          <Field label="훅 스타일">
            <Select value={hook} onChange={e => setHook(e.target.value)}
              options={[
                { value: 'question',  label: '질문형 ("...아셨나요?")' },
                { value: 'shock',     label: '충격 사실형'              },
                { value: 'story',     label: '미스터리 오프닝'           },
                { value: 'list',      label: '리스트형 ("3가지 이유")'    },
              ]}
            />
          </Field>

          <Field label="추가 지시사항" hint="선택사항">
            <textarea
              placeholder="예: 30대 남성 타겟, 친근한 반말 톤"
              rows={3}
              style={{
                background: T.panel, border: `1px solid ${T.border}`,
                borderRadius: 7, padding: '8px 10px', resize: 'none',
                color: T.text, fontSize: 12, fontFamily: T.font,
                outline: 'none', lineHeight: 1.5,
              }}
            />
          </Field>

          <div style={{ flex: 1 }} />

          <Button variant="primary" icon="spark" size="lg" onClick={generate} disabled={generating}>
            {generating ? `생성 중 ${progress}%` : '대본 생성'}
          </Button>
          {generating && (
            <div style={{ height: 3, background: T.panel3, borderRadius: 2, overflow: 'hidden' }}>
              <div style={{ height: '100%', width: `${progress}%`, background: T.accent, transition: 'width 80ms linear' }} />
            </div>
          )}
        </div>

        {/* Editor */}
        <div style={{ display: 'flex', flexDirection: 'column', minWidth: 0 }}>
          <div style={{
            display: 'flex', alignItems: 'center', justifyContent: 'space-between',
            padding: '14px 24px', borderBottom: `1px solid ${T.border}`,
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
              <span style={{ fontSize: 13, fontWeight: 600, color: T.text }}>script_v3.md</span>
              <Tag color={T.green} bg={T.green + '14'}>저장됨</Tag>
              <Tag color={T.textDim}>1,247자</Tag>
              <Tag color={T.textDim}>약 4분 52초</Tag>
            </div>
            <div style={{ display: 'flex', gap: 8 }}>
              <Button variant="ghost"     size="sm" icon="edit">재생성</Button>
              <Button variant="secondary" size="sm" icon="upload">업로드 탭으로</Button>
            </div>
          </div>

          <div style={{ flex: 1, overflow: 'auto', padding: '20px 32px' }}>
            <textarea
              value={script}
              onChange={e => setScript(e.target.value)}
              style={{
                width: '100%', height: '100%',
                background: 'transparent', border: 'none', outline: 'none',
                color: T.text, fontSize: 14, lineHeight: 1.7,
                fontFamily: T.mono, resize: 'none',
                whiteSpace: 'pre-wrap',
              }}
            />
          </div>

          <div style={{
            display: 'flex', justifyContent: 'space-between',
            padding: '10px 24px', borderTop: `1px solid ${T.border}`,
            fontSize: 11, color: T.textMute, fontFamily: T.mono,
          }}>
            <span>UTF-8 · Markdown · LF</span>
            <span>Ln 14, Col 28 · Claude Sonnet 4.5</span>
          </div>
        </div>
      </div>
    </div>
  );
}

window.ScriptTab = ScriptTab;
