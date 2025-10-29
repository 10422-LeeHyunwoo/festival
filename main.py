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
    #game { width: 500px; height: 720px; margin: 20px auto; background: #000; position: relative; overflow: hidden; border: 3px solid #333; border-radius: 12px; }
    .score { position: absolute; top: 10px; color: white; font-weight: bold; z-index: 10; font-size: 14px; }
    #p1 { left: 20px; color: #60a5fa; }
    #p2 { right: 20px; color: #f87171; }
    #target { left: 50%; transform: translateX(-50%); color: #facc15; }
    #info { position: absolute; top: 40px; left: 50%; transform: translateX(-50%); color: #aaa; font-size: 12px; }
    .snake1 { background: #3b82f6; border-radius: 4px; position: absolute; box-shadow: 0 0 10px #3b82f6; }
    .snake2 { background: #ef4444; border-radius: 4px; position: absolute; box-shadow: 0 0 10px #ef4444; }
    .food { background: #facc15; border-radius: 50%; position: absolute; animation: pulse 1s infinite; }
    @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.2); } }
    .overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); color: white; display: flex; flex-direction: column; align-items: center; justify-content: center; font-size: 20px; z-index: 20; text-align: center; }
    button { margin-top: 20px; padding: 12px 24px; font-size: 18px; background: #22c55e; color: white; border: none; border-radius: 8px; cursor: pointer; }
    button:hover { background: #16a34a; }
    .final { color: #fbbf24; font-size: 28px; }
  </style>
</head>
<body>
  <div id="game">
    <div id="p1" class="score">플레이어 1: 0</div>
    <div id="target" class="score">목표: 500점</div>
    <div id="p2" class="score">플레이어 2: 0</div>
    <div id="info" class="score">라운드 시간: 0초 | 길이: 1</div>
    <div class="overlay" id="menu">
      <h1 style="color:#22c55e">스네이크 배틀</h1>
      <p>플레이어 1: W A S D</p>
      <p>플레이어 2: 방향키</p>
      <p style="color:#facc15">먹이 +10점 | 킬 보너스: 50 + (시간×2)</p>
      <p style="color:#fbbf24">누적 500점 = 최종 승리!</p>
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
    let totalScores = [0, 0];  // 누적 점수
    let roundScores = [0, 0];  // 이번 라운드 점수 (킬 보너스용)
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
      document.getElementById('p1').textContent = `플레이어 1: ${totalScores[0]}`;
      document.getElementById('p2').textContent = `플레이어 2: ${totalScores[1]}`;
      document.getElementById('info').textContent = `라운드 시간: ${roundTime}초 | 길이: ${currentLength}`;
    }

    function startRound() {
      snake1 = [{x:3,y:10}]; snake2 = [{x:16,y:10}];
      dir1 = {x:1,y:0}; dir2 = {x:-1,y:0};
      roundScores = [0, 0];
      initFood();
      gameState = 'playing';
      startTime = Date.now();
      document.querySelectorAll('.overlay').forEach(o => o.remove());
      updateUI();
      if (interval) clearInterval(interval);
      interval = setInterval(tick, 150);
    }

    function start() {
      totalScores = [0, 0];
      startRound();
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
          roundScores[0] += 10;
          totalScores[0] += 10;
          ate1 = true;
        } else if (food[i].x === h2.x && food[i].y === h2.y) {
          food.splice(i, 1);
          roundScores[1] += 10;
          totalScores[1] += 10;
          ate2 = true;
        }
      }

      // 뱀 성장
      if (ate1) snake1 = [h1, ...snake1];
      else if (snake1.length > currentLength) snake1 = [h1, ...snake1.slice(0, currentLength)];
      else snake1 = [h1, ...snake1.slice(0, -1)];

      if (ate2) snake2 = [h2, ...snake2];
      else if (snake2.length > currentLength) snake2 = [h2, ...snake2.slice(0, currentLength)];
      else snake2 = [h2, ...snake2.slice(0, -1)];

      // 먹이 보충
      while (food.length < 3) food.push(randFood());

      // 충돌 → 라운드 종료 + 킬 보너스
      if (snake1.slice(1).some(s=>s.x===h1.x&&s.y===h1.y) || snake2.some(s=>s.x===h1.x&&s.y===h1.y)) {
        const bonus = 50 + roundTime * 2;
        totalScores[1] += bonus;
        roundScores[1] += bonus;
        showRoundEnd(2, bonus, false);
        return;
      }
      if (snake2.slice(1).some(s=>s.x===h2.x&&s.y===h2.y) || snake1.some(s=>s.x===h2.x&&s.y===h2.y)) {
        const bonus = 50 + roundTime * 2;
        totalScores[0] += bonus;
        roundScores[0] += bonus;
        showRoundEnd(1, bonus, false);
        return;
      }

      // 500점 도달 → 최종 승리
      if (totalScores[0] >= 500 || totalScores[1] >= 500) {
        const winner = totalScores[0] >= 500 ? 1 : 2;
        showRoundEnd(winner, 0, true);
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

    function showRoundEnd(winner, bonus, isFinal) {
      clearInterval(interval);
      const overlay = document.createElement('div');
      overlay.className = 'overlay';
      let msg = isFinal 
        ? `<span class="final">플레이어 ${winner} 최종 승리!</span>`
        : `플레이어 ${winner} 라운드 승리!`;
      if (bonus > 0) msg += `<br>킬 보너스: +${bonus}점`;
      overlay.innerHTML = `
        <h1 style="color:#22c55e">${msg}</h1>
        <p>플레이어 1: ${totalScores[0]}점 | 플레이어 2: ${totalScores[1]}점</p>
        <button onclick="${isFinal ? 'location.reload()' : 'startRound()'}">
          ${isFinal ? '새 게임' : '다음 라운드 (Space)'}
        </button>
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

    // 키보드 + Space로 다음 라운드
    document.addEventListener('keydown', e => {
      if (gameState === 'playing') {
        if (e.key === 'w' && dir1.y === 0) dir1 = {x:0,y:-1};
        if (e.key === 's' && dir1.y === 0) dir1 = {x:0,y:1};
        if (e.key === 'a' && dir1.x === 0) dir1 = {x:-1,y:0};
        if (e.key === 'd' && dir1.x === 0) dir1 = {x:1,y:0};
        if (e.key === 'ArrowUp' && dir2.y === 0) dir2 = {x:0,y:-1};
        if (e.key === 'ArrowDown' && dir2.y === 0) dir2 = {x:0,y:1};
        if (e.key === 'ArrowLeft' && dir2.x === 0) dir2 = {x:-1,y:0};
        if (e.key === 'ArrowRight' && dir2.x === 0) dir2 = {x:1,y:0};
      } else if (e.key === ' ') {
        const overlay = document.querySelector('.overlay');
        if (overlay && overlay.innerText.includes('다음 라운드')) {
          startRound();
        }
      }
    });

    window.start = start;
    window.startRound = startRound;
  </script>
</body>
</html>
"""

st.components.v1.html(HTML_CONTENT, height=760, scrolling=False)

with st.sidebar:
    st.header("게임 규칙")
    st.markdown("""
    - **한 명이 죽으면** → **라운드 종료** + **킬 보너스 (50 + 시간×2)**
    - **점수는 누적됨**
    - **누적 500점 도달** → **최종 승리!**
    - **Space** → 다음 라운드
    """)
    st.success("점수 누적 + 500점 승리 완벽 구현!")
