# main.py
import streamlit as st

st.set_page_config(page_title="스네이크 배틀", layout="centered")

st.write("게임 로딩 중...")

HTML_CONTENT = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>스네이크 배틀</title>
  <style>
    body, html { margin:0; padding:0; height:100%; background:#111; font-family: sans-serif; }
    #game { width: 500px; height: 680px; margin: 20px auto; background: #000; position: relative; overflow: hidden; border: 3px solid #333; border-radius: 12px; }
    .score { position: absolute; top: 10px; color: white; font-weight: bold; z-index: 10; font-size: 14px; }
    #p1 { left: 20px; color: #60a5fa; }
    #p2 { right: 20px; color: #f87171; }
    #target { left: 50%; transform: translateX(-50%); color: #facc15; }
    #info { position: absolute; top: 40px; left: 50%; transform: translateX(-50%); color: #aaa; font-size: 12px; }
    .snake1 { background: #3b82f6; border-radius: 4px; position: absolute; box-shadow: 0 0 10px #3b82f6; }
    .snake2 { background: #ef4444; border-radius: 4px; position: absolute; box-shadow: 0 0 10px #ef4444; }
    .food { background: #facc15; border-radius: 50%; position: absolute; animation: pulse 1s infinite; }
    @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.2); } }
    .overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); color: white; display: flex; flex-direction: column; align-items: center; justify-content: center; font-size: 20px; z-index: 20; }
    button { margin-top: 20px; padding: 12px 24px; font-size: 18px; background: #22c55e; color: white; border: none; border-radius: 8px; cursor: pointer; }
    button:hover { background: #16a34a; }
  </style>
</head>
<body>
  <div id="game">
    <div id="p1" class="score">플레이어 1: 0</div>
    <div id="target" class="score">목표: 500점</div>
    <div id="p2" class="score">플레이어 2: 0</div>
    <div id="info" class="score">길이: 1 | 시간: 0초</div>
    <div class="overlay" id="menu">
      <h1 style="color:#22c55e">스네이크 배틀</h1>
      <p>플레이어 1: W A S D</p>
      <p>플레이어 2: 방향키</p>
      <p style="color:#facc15">먹이 1개 = +10점 | 2초마다 길이 +1</p>
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
    let scores = [0, 0];
    let gameState = 'menu';
    let interval;
    let startTime = 0;
    let roundTime = 0;
    let currentLength = 1;

    function initFood() {
      food = [];
      for(let i=0; i<3; i++) {
        let f;
        do { f = {x: Math.floor(Math.random()*GRID), y: Math.floor(Math.random()*GRID)} }
        while (snake1.some(s=>s.x===f.x&&s.y===f.y) || snake2.some(s=>s.x===f.x&&s.y===f.y) || food.some(ff=>ff.x===f.x&&ff.y===f.y));
        food.push(f);
      }
    }

    function updateUI() {
      document.getElementById('p1').textContent = `플레이어 1: ${scores[0]}`;
      document.getElementById('p2').textContent = `플레이어 2: ${scores[1]}`;
      document.getElementById('info').textContent = `길이: ${currentLength} | 시간: ${roundTime}초`;
    }

    function start() {
      snake1 = [{x:3,y:10}]; snake2 = [{x:16,y:10}];
      dir1 = {x:1,y:0}; dir2 = {x:-1,y:0};
      scores = [0, 0];
      currentLength = 1;
      initFood();
      gameState = 'playing';
      startTime = Date.now();
      document.getElementById('menu').style.display = 'none';
      updateUI();
      if (interval) clearInterval(interval);
      interval = setInterval(tick, 150);
    }

    function tick() {
      const now = Date.now();
      const elapsed = (now - startTime) / 1000;
      roundTime = Math.floor(elapsed);
      currentLength = Math.floor(elapsed / 2) + 1;

      // 이동
      let h1 = { x: (snake1[0].x + dir1.x + GRID) % GRID, y: (snake1[0].y + dir1.y + GRID) % GRID };
      let h2 = { x: (snake2[0].x + dir2.x + GRID) % GRID, y: (snake2[0].y + dir2.y + GRID) % GRID };

      let ate1 = false, ate2 = false;

      // 먹이 먹기
      for (let i = food.length - 1; i >= 0; i--) {
        if (food[i].x === h1.x && food[i].y === h1.y) {
          food.splice(i, 1);
          scores[0] += 10;
          ate1 = true;
        } else if (food[i].x === h2.x && food[i].y === h2.y) {
          food.splice(i, 1);
          scores[1] += 10;
          ate2 = true;
        }
      }

      // 뱀 성장 (먹이 먹으면 길이 유지, 아니면 currentLength로 자름)
      if (ate1) {
        snake1 = [h1, ...snake1];  // 먹으면 길이 +1
      } else {
        // currentLength보다 길면 자름
        if (snake1.length > currentLength) {
          snake1 = [h1, ...snake1.slice(0, currentLength)];
        } else {
          snake1 = [h1, ...snake1.slice(0, -1)];
        }
      }

      if (ate2) {
        snake2 = [h2, ...snake2];
      } else {
        if (snake2.length > currentLength) {
          snake2 = [h2, ...snake2.slice(0, currentLength)];
        } else {
          snake2 = [h2, ...snake2.slice(0, -1)];
        }
      }

      // 먹이 보충
      while (food.length < 3) {
        food.push(randFood());
      }

      // 충돌 체크
      if (snake1.slice(1).some(s=>s.x===h1.x&&s.y===h1.y) || snake2.some(s=>s.x===h1.x&&s.y===h1.y)) {
        const bonus = 50 + roundTime * 2;
        scores[1] += bonus;
        end(`플레이어 2 승리! +${bonus}점`, scores[1] >= 500);
        return;
      }
      if (snake2.slice(1).some(s=>s.x===h2.x&&s.y===h2.y) || snake1.some(s=>s.x===h2.x&&s.y===h2.y)) {
        const bonus = 50 + roundTime * 2;
        scores[0] += bonus;
        end(`플레이어 1 승리! +${bonus}점`, scores[0] >= 500);
        return;
      }

      // 500점 승리
      if (scores[0] >= 500 || scores[1] >= 500) {
        end(scores[0] >= 500 ? "플레이어 1 최종 승리!" : "플레이어 2 최종 승리!", true);
        return;
      }

      updateUI();
      render();
    }

    function randFood() {
      let f;
      do { f = {x: Math.floor(Math.random()*GRID), y: Math.floor(Math.random()*GRID)} }
      while (snake1.some(s=>s.x===f.x&&s.y===f.y) || snake2.some(s=>s.x===f.x&&s.y===f.y) || food.some(ff=>ff.x===f.x&&ff.y===f.y));
      return f;
    }

    function end(msg, isFinal) {
      clearInterval(interval);
      const overlay = document.createElement('div');
      overlay.className = 'overlay';
      overlay.innerHTML = `
        <h1 style="color:#22c55e">${msg}</h1>
        <p>플레이어 1: ${scores[0]}점 | 플레이어 2: ${scores[1]}점</p>
        <p>최대 길이: ${currentLength}</p>
        <button onclick="location.reload()">${isFinal ? '새 게임' : '다음 라운드'}</button>
      `;
      document.getElementById('game').appendChild(overlay);
    }

    function render() {
      const game = document.getElementById('game');
      game.querySelectorAll('.snake1, .snake2, .food').forEach(e=>e.remove());

      snake1.forEach((s,i) => {
        const el = document.createElement('div');
        el.className = 'snake1';
        el.style.left = s.x * SIZE + 'px';
        el.style.top = s.y * SIZE + 100 + 'px';
        el.style.width = el.style.height = (SIZE-2) + 'px';
        if (i===0) el.style.boxShadow = '0 0 12px #3b82f6';
        game.appendChild(el);
      });

      snake2.forEach((s,i) => {
        const el = document.createElement('div');
        el.className = 'snake2';
        el.style.left = s.x * SIZE + 'px';
        el.style.top = s.y * SIZE + 100 + 'px';
        el.style.width = el.style.height = (SIZE-2) + 'px';
        if (i===0) el.style.boxShadow = '0 0 12px #ef4444';
        game.appendChild(el);
      });

      food.forEach(f => {
        const el = document.createElement('div');
        el.className = 'food';
        el.style.left = f.x * SIZE + 4 + 'px';
        el.style.top = f.y * SIZE + 104 + 'px';
        el.style.width = el.style.height = (SIZE-8) + 'px';
        game.appendChild(el);
      });
    }

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

    window.start = start;
  </script>
</body>
</html>
"""

st.components.v1.html(HTML_CONTENT, height=720, scrolling=False)

with st.sidebar:
    st.header("게임 규칙")
    st.markdown("""
    - **먹이 먹기** → **+10점** + **길이 +1**
    - **2초마다** → **길이 자동 +1**
    - **상대 죽이기** → **50 + (시간×2)점**
    - **500점 먼저** → **최종 승리!**
    """)
    st.success("몸 길이가 실시간으로 늘어납니다!")
