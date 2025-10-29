# main.py
import streamlit as st

st.set_page_config(page_title="스네이크 배틀", page_icon="snake", layout="centered")

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>스네이크 배틀</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body { margin: 0; padding: 0; background: #0f172a; }
    #game { max-width: 600px; margin: 0 auto; }
  </style>
</head>
<body>
  <div id="root"></div>

  <script type="module">
    import React from "https://esm.sh/react@18";
    import ReactDOM from "https://esm.sh/react-dom@18";
    import { Play, RotateCcw, Trophy } from "https://esm.sh/lucide-react";

    const { useState, useEffect, useRef } = React;

    function SnakeBattle() {
      const [gameState, setGameState] = useState('menu');
      const [snake1, setSnake1] = useState([{ x: 3, y: 10 }]);
      const [snake2, setSnake2] = useState([{ x: 16, y: 10 }]);
      const [dir1, setDir1] = useState({ x: 1, y: 0 });
      const [dir2, setDir2] = useState({ x: -1, y: 0 });
      const [food, setFood] = useState([]);
      const [scores, setScores] = useState([0, 0]);
      const [winner, setWinner] = useState('');
      const [roundTime, setRoundTime] = useState(0);
      const [currentLength, setCurrentLength] = useState(1);

      const GRID_SIZE = 20;
      const CELL_SIZE = 25;
      const gameLoopRef = useRef(null);
      const nextDir1 = useRef({ x: 1, y: 0 });
      const nextDir2 = useRef({ x: -1, y: 0 });
      const startTimeRef = useRef(0);

      const generateFood = (s1, s2) => {
        const pos = { x: Math.floor(Math.random() * GRID_SIZE), y: Math.floor(Math.random() * GRID_SIZE) };
        if (s1.some(p => p.x === pos.x && p.y === pos.y) || s2.some(p => p.x === pos.x && p.y === pos.y)) {
          return generateFood(s1, s2);
        }
        return pos;
      };

      const startGame = () => {
        const s1 = [{ x: 3, y: 10 }];
        const s2 = [{ x: 16, y: 10 }];
        setSnake1(s1); setSnake2(s2);
        setDir1({ x: 1, y: 0 }); setDir2({ x: -1, y: 0 });
        nextDir1.current = { x: 1, y: 0 }; nextDir2.current = { x: -1, y: 0 };
        const foods = Array(3).fill().map(() => generateFood(s1, s2));
        setFood(foods);
        setScores([0, 0]);
        setWinner('');
        setRoundTime(0);
        setCurrentLength(1);
        startTimeRef.current = Date.now();
        setGameState('playing');
      };

      useEffect(() => {
        const onKey = (e) => {
          if (gameState !== 'playing') {
            if (e.key === ' ') startGame();
            if (e.key === 'r') { setScores([0, 0]); setGameState('menu'); }
            return;
          }
          // Player 1
          if (e.key === 'w' && dir1.y !== 1) nextDir1.current = { x: 0, y: -1 };
          if (e.key === 's' && dir1.y !== -1) nextDir1.current = { x: 0, y: 1 };
          if (e.key === 'a' && dir1.x !== 1) nextDir1.current = { x: -1, y: 0 };
          if (e.key === 'd' && dir1.x !== -1) nextDir1.current = { x: 1, y: 0 };
          // Player 2
          if (e.key === 'ArrowUp' && dir2.y !== 1) nextDir2.current = { x: 0, y: -1 };
          if (e.key === 'ArrowDown' && dir2.y !== -1) nextDir2.current = { x: 0, y: 1 };
          if (e.key === 'ArrowLeft' && dir2.x !== 1) nextDir2.current = { x: -1, y: 0 };
          if (e.key === 'ArrowRight' && dir2.x !== -1) nextDir2.current = { x: 1, y: 0 };
        };
        window.addEventListener('keydown', onKey);
        return () => window.removeEventListener('keydown', onKey);
      }, [gameState, dir1, dir2]);

      useEffect(() => {
        if (gameState !== 'playing') return;

        let prevS1 = snake1;
        let prevS2 = snake2;
        let curFood = food;

        const move = () => {
          const now = Date.now();
          const elapsed = (now - startTimeRef.current) / 1000;
          const time = Math.floor(elapsed);
          const length = Math.floor(elapsed / 2) + 1;
          setRoundTime(time);
          setCurrentLength(length);

          setDir1(nextDir1.current);
          setDir2(nextDir2.current);

          // Snake 1
          const h1 = prevS1[0];
          const nh1 = { x: (h1.x + nextDir1.current.x + GRID_SIZE) % GRID_SIZE, y: (h1.y + nextDir1.current.y + GRID_SIZE) % GRID_SIZE };
          let ate1 = curFood.findIndex(f => f.x === nh1.x && f.y === nh1.y);
          let ns1 = ate1 !== -1 ? [nh1, ...prevS1] : [nh1, ...prevS1.slice(0, -length)];
          if (ate1 !== -1) curFood = curFood.filter((_, i) => i !== ate1);

          if (ns1.slice(1).some(s => s.x === nh1.x && s.y === nh1.y) || prevS2.some(s => s.x === nh1.x && s.y === nh1.y)) {
            const killBonus = 50 + time * 2;
            setScores(prev => [prev[0], prev[1] + killBonus]);
            if (scores[1] + killBonus >= 500) {
              setWinner('플레이어 2 최종 승리! Trophy'); setGameState('gameover');
            } else {
              setWinner(`플레이어 2 라운드 승리! +${killBonus}점`); setGameState('gameover');
            }
            return;
          }

          // Snake 2
          const h2 = prevS2[0];
          const nh2 = { x: (h2.x + nextDir2.current.x + GRID_SIZE) % GRID_SIZE, y: (h2.y + nextDir2.current.y + GRID_SIZE) % GRID_SIZE };
          let ate2 = curFood.findIndex(f => f.x === nh2.x && f.y === nh2.y);
          let ns2 = ate2 !== -1 ? [nh2, ...prevS2] : [nh2, ...prevS2.slice(0, -length)];
          if (ate2 !== -1) curFood = curFood.filter((_, i) => i !== ate2);

          if (ns2.slice(1).some(s => s.x === nh2.x && s.y === nh2.y) || ns1.some(s => s.x === nh2.x && s.y === nh2.y)) {
            const killBonus = 50 + time * 2;
            setScores(prev => [prev[0] + killBonus, prev[1]]);
            if (scores[0] + killBonus >= 500) {
              setWinner('플레이어 1 최종 승리! Trophy'); setGameState('gameover');
            } else {
              setWinner(`플레이어 1 라운드 승리! +${killBonus}점`); setGameState('gameover');
            }
            return;
          }

          // 먹이 보충
          if (curFood.length < 3) {
            curFood.push(generateFood(ns1, ns2));
          }

          // 점수 증가
          if (ate1 !== -1) setScores(prev => [prev[0] + 10, prev[1]]);
          if (ate2 !== -1) setScores(prev => [prev[0], prev[1] + 10]);

          // 500점 승리 체크
          if (scores[0] >= 500 || scores[1] >= 500) {
            setGameState('gameover');
            setWinner(scores[0] >= 500 ? '플레이어 1 최종 승리! Trophy' : '플레이어 2 최종 승리! Trophy');
          }

          prevS1 = ns1; prevS2 = ns2;
          setSnake1(ns1); setSnake2(ns2); setFood(curFood);
        };

        gameLoopRef.current = setInterval(move, 100);
        return () => clearInterval(gameLoopRef.current);
      }, [gameState]);

      return React.createElement('div', { className: "min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center p-4" },
        React.createElement('div', { id: 'game', className: "w-full" },
          // 점수판
          React.createElement('div', { className: "bg-gray-800 rounded-t-2xl p-4 flex justify-between text-white text-sm font-bold" },
            React.createElement('div', { className: "text-blue-400" }, `플레이어 1: ${scores[0]}`),
            React.createElement('div', {}, `목표: 500점`),
            React.createElement('div', { className: "text-red-400" }, `플레이어 2: ${scores[1]}`)
          ),
          gameState === 'playing' && React.createElement('div', { className: "bg-gray-800 px-4 pb-2 text-xs text-center text-gray-300" },
            `시간: ${roundTime}초 | 킬 보너스: ${50 + roundTime * 2}점 | 길이: ${currentLength}`
          ),

          // 게임 보드
          React.createElement('div', { className: "relative bg-black rounded-b-2xl overflow-hidden", style: { height: GRID_SIZE * CELL_SIZE + 100 } },
            // 먹이
            food.map((f, i) => React.createElement('div', {
              key: `f${i}`, className: "absolute bg-yellow-400 rounded-full animate-pulse",
              style: { left: f.x * CELL_SIZE + 1, top: f.y * CELL_SIZE + 101, width: CELL_SIZE - 2, height: CELL_SIZE - 2 }
            })),
            // Snake 1
            snake1.map((s, i) => React.createElement('div', {
              key: `s1${i}`, className: "absolute rounded",
              style: { left: s.x * CELL_SIZE + 1, top: s.y * CELL_SIZE + 101, width: CELL_SIZE - 2, height: CELL_SIZE - 2,
                backgroundColor: i === 0 ? '#3b82f6' : '#60a5fa', boxShadow: i === 0 ? '0 0 10px #3b82f6' : 'none'
              }
            })),
            // Snake 2
            snake2.map((s, i) => React.createElement('div', {
              key: `s2${i}`, className: "absolute rounded",
              style: { left: s.x * CELL_SIZE + 1, top: s.y * CELL_SIZE + 101, width: CELL_SIZE - 2, height: CELL_SIZE - 2,
                backgroundColor: i === 0 ? '#ef4444' : '#f87171', boxShadow: i === 0 ? '0 0 10px #ef4444' : 'none'
              }
            })),

            // 오버레이
            gameState !== 'playing' && React.createElement('div', { className: "absolute inset-0 bg-black bg-opacity-80 flex flex-col items-center justify-center text-center p-4" },
              gameState === 'menu' ? [
                React.createElement('h1', { key: 'title', className: "text-4xl font-bold text-green-400 mb-4" }, "스네이크 배틀"),
                React.createElement('div', { key: 'p1', className: "text-blue-400" }, "플레이어 1: W A S D"),
                React.createElement('div', { key: 'p2', className: "text-red-400" }, "플레이어 2: 방향키"),
                React.createElement('div', { key: 'start', className: "text-yellow-400 mt-2" }, "스페이스바로 시작!")
              ] : [
                React.createElement('div', { key: 'win', className: "text-3xl font-bold text-green-400 mb-2" }, winner),
                React.createElement('div', { key: 'next', className: "text-gray-300" }, "스페이스: 다음 라운드 | R: 점수 초기화")
              ]
            )
          ),

          // 버튼
          React.createElement('div', { className: "flex gap-4 justify-center mt-4" }, [
            React.createElement('button', { onClick: startGame, className: "bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg font-bold flex items-center gap-2" },
              React.createElement(Play, { size: 18 }), gameState === 'menu' ? '게임 시작' : '재시작'
            ),
            React.createElement('button', { onClick: () => { setScores([0,0]); setGameState('menu'); }, className: "bg-gray-600 hover:bg-gray-700 text-white px-6 py-2 rounded-lg font-bold flex items-center gap-2" },
              React.createElement(RotateCcw, { size: 18 }), '메뉴'
            )
          ])
        )
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(React.createElement(SnakeBattle));
  </script>
</body>
</html>
"""

st.components.v1.html(HTML_CONTENT, height=750, scrolling=False)

with st.sidebar:
    st.header("조작법")
    st.markdown("""
    - **Player 1**: `W` `A` `S` `D`
    - **Player 2**: `↑` `↓` `←` `→`
    - **시작/재시작**: `Space`
    - **점수 초기화**: `R`
    """)
    st.success("500점 먼저 도달하면 최종 승리!")
