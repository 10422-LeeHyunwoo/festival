# main.py
import streamlit as st

st.set_page_config(page_title="스네이크 배틀", layout="centered")

# 디버그: HTML이 제대로 들어가는지 확인
st.write("게임 로딩 중... (화면 아래에 게임이 나타납니다)")

# 최소한의 HTML + JS (React 없이도 동작 보장)
HTML_CONTENT = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>스네이크 배틀</title>
  <style>
    body, html { margin:0; padding:0; height:100%; background:#111; font-family: sans-serif; }
    #game { width: 500px; height: 600px; margin: 20px auto; background: #000; position: relative; overflow: hidden; border: 3px solid #333; border-radius: 12px; }
    .snake1 { background: #3b82f6; border-radius: 4px; position: absolute; box-shadow: 0 0 8px #3b82f6; }
    .snake2 { background: #ef4444; border-radius: 4px; position: absolute; box-shadow: 0 0 8px #ef4444; }
    .food { background: #facc15; border-radius: 50%; position: absolute; }
    .overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); color: white; display: flex; flex-direction: column; align-items: center; justify-content: center; font-size: 20px; }
    button { margin-top: 20px; padding: 10px 20px; font-size: 18px; background: #22c55e; color: white; border: none; border-radius: 8px; cursor: pointer; }
    button:hover { background: #16a34a; }
  </style>
</head>
<body>
  <div id="game">
    <div class="overlay" id="menu">
      <h1 style="color:#22c55e">스네이크 배틀</h1>
      <p>플레이어 1: W A S D</p>
      <p>플레이어 2: 방향키</p>
      <button onclick="start()">게임 시작</button>
    </div>
  </div>

  <script>
    const GRID = 20;
    const SIZE = 25;
    let snake1 = [{x:3,y:10}];
    let snake2 = [{x:16,y:10}];
    let dir1 = {x:1,y:0};
    let dir2 = {x:-1,y:0};
    let food = [];
    let gameState = 'menu';
    let interval;

    function initFood() {
      food = [];
      for(let i=0; i<3; i++) {
        let f;
        do { f = {x: Math.floor(Math.random()*GRID), y: Math.floor(Math.random()*GRID)} }
        while (snake1.some(s=>s.x===f.x&&s.y===f.y) || snake2.some(s=>s.x===f.x&&s.y===f.y) || food.some(ff=>ff.x===f.x&&ff.y===f.y));
        food.push(f);
      }
    }

    function start() {
      snake1 = [{x:3,y:10}]; snake2 = [{x:16,y:10}];
      dir1 = {x:1,y:0}; dir2 = {x:-1,y:0};
      initFood();
      gameState = 'playing';
      document.getElementById('menu').style.display = 'none';
      if (interval) clearInterval(interval);
      interval = setInterval(tick, 150);
    }

    function tick() {
      // 이동
      let h1 = { x: (snake1[0].x + dir1.x + GRID) % GRID, y: (snake1[0].y + dir1.y + GRID) % GRID };
      let h2 = { x: (snake2[0].x + dir2.x + GRID) % GRID, y: (snake2[0].y + dir2.y + GRID) % GRID };

      // 먹이
      if (food.some((f,i) => { if (f.x===h1.x && f.y===h1.y) { food.splice(i,1); return true; } return false; })) {
        snake1 = [h1, ...snake1];
        if (food.length < 3) food.push(randFood());
      } else snake1 = [h1, ...snake1.slice(0,-1)];

      if (food.some((f,i) => { if (f.x===h2.x && f.y===h2.y) { food.splice(i,1); return true; } return false; })) {
        snake2 = [h2, ...snake2];
        if (food.length < 3) food.push(randFood());
      } else snake2 = [h2, ...snake2.slice(0,-1)];

      // 충돌
      if (snake1.slice(1).some(s=>s.x===h1.x&&s.y===h1.y) || snake2.some(s=>s.x===h1.x&&s.y===h1.y)) {
        end("플레이어 2 승리!");
      }
      if (snake2.slice(1).some(s=>s.x===h2.x&&s.y===h2.y) || snake1.some(s=>s.x===h2.x&&s.y===h2.y)) {
        end("플레이어 1 승리!");
      }

      render();
    }

    function randFood() {
      let f;
      do { f = {x: Math.floor(Math.random()*GRID), y: Math.floor(Math.random()*GRID)} }
      while (snake1.some(s=>s.x===f.x&&s.y===f.y) || snake2.some(s=>s.x===f.x&&s.y===f.y) || food.some(ff=>ff.x===f.x&&ff.y===f.y));
      return f;
    }

    function end(msg) {
      clearInterval(interval);
      const overlay = document.createElement('div');
      overlay.className = 'overlay';
      overlay.innerHTML = `<h1 style="color:#22c55e">${msg}</h1><button onclick="location.reload()">다시 시작</button>`;
      document.getElementById('game').appendChild(overlay);
    }

    function render() {
      const game = document.getElementById('game');
      // 기존 제거
      game.querySelectorAll('.snake1, .snake2, .food').forEach(e=>e.remove());

      // 뱀1
      snake1.forEach((s,i) => {
        const el = document.createElement('div');
        el.className = 'snake1';
        el.style.left = s.x * SIZE + 'px';
        el.style.top = s.y * SIZE + 100 + 'px';
        el.style.width = el.style.height = (SIZE-2) + 'px';
        if (i===0) el.style.boxShadow = '0 0 12px #3b82f6';
        game.appendChild(el);
      });

      // 뱀2
      snake2.forEach((s,i) => {
        const el = document.createElement('div');
        el.className = 'snake2';
        el.style.left = s.x * SIZE + 'px';
        el.style.top = s.y * SIZE + 100 + 'px';
        el.style.width = el.style.height = (SIZE-2) + 'px';
        if (i===0) el.style.boxShadow = '0 0 12px #ef4444';
        game.appendChild(el);
      });

      // 먹이
      food.forEach(f => {
        const el = document.createElement('div');
        el.className = 'food';
        el.style.left = f.x * SIZE + 4 + 'px';
        el.style.top = f.y * SIZE + 104 + 'px';
        el.style.width = el.style.height = (SIZE-8) + 'px';
        game.appendChild(el);
      });
    }

    // 키보드
    document.addEventListener('keydown', e => {
      if (gameState !== 'playing') return;
      if (e.key === 'w' && dir1.y === 0) dir1 = {x:0,y:-1};
      if (e.key === 's' && dir1.y === 0) dir1 = {x:0,y:1};
      if (e.key === 'a' && dir1.x === 0) dir1 = {x:-1,y:0};
      if (e.key === 'd' && dir1.x === 0) dir1 = {x:1,y:0};
      if (e.key === 'ArrowUp' && dir2.y === 0) dir2 = {x:0,y:-1};
      if (e.key === 'ArrowDown' && dir2.y === 0) dir2 = {x:0,y:1};
      if (e.key === 'ArrowLeft' && dir2.x === 0) dir2 = {x:-1,y:0};
      if (e.key === 'ArrowRight' && dir2.x === 0) dir2 = {x:1,y:0};
    });

    // 시작 화면
    window.start = start;
  </script>
</body>
</html>
"""

# 핵심: height를 고정, scrolling=False
st.components.v1.html(HTML_CONTENT, height=650, scrolling=False)

# 사이드바
with st.sidebar:
    st.header("조작법")
    st.markdown("""
    - **Player 1**: `W` `A` `S` `D`
    - **Player 2**: `↑` `↓` `←` `→`
    - **게임 시작**: 버튼 클릭
    """)
    st.success("화면이 뜨면 게임 시작!")
