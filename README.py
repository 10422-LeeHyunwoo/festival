# main.py
import streamlit as st

st.set_page_config(page_title="Snake Battle", page_icon="snake", layout="centered")

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Snake Battle</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
  <div id="root"></div>

  <script type="module">
    import React from "https://esm.sh/react@18";
    import ReactDOM from "https://esm.sh/react-dom@18";
    import { Play, RotateCcw } from "https://esm.sh/lucide-react";

    const { useState, useEffect, useRef } = React;

    function SnakeBattle() {
      const [gameState, setGameState] = useState('menu');
      const [snake1, setSnake1] = useState([{ x: 5, y: 10 }]);
      const [snake2, setSnake2] = useState([{ x: 25, y: 10 }]);
      const [direction1, setDirection1] = useState({ x: 1, y: 0 });
      const [direction2, setDirection2] = useState({ x: -1, y: 0 });
      const [food, setFood] = useState([]);
      const [winner, setWinner] = useState('');

      const gridSize = 30;
      const cellSize = 15;
      const gameLoopRef = useRef(null);
      const nextDirection1 = useRef({ x: 1, y: 0 });
      const nextDirection2 = useRef({ x: -1, y: 0 });

      const generateFood = (s1, s2) => {
        const newFood = [];
        for (let i = 0; i < 3; i++) {
          let pos;
          let tries = 0;
          do {
            pos = { x: Math.floor(Math.random() * gridSize), y: Math.floor(Math.random() * gridSize) };
            tries++;
          } while (tries < 100 && (
            s1.some(p => p.x === pos.x && p.y === pos.y) ||
            s2.some(p => p.x === pos.x && p.y === pos.y) ||
            newFood.some(f => f.x === pos.x && f.y === pos.y)
          ));
          newFood.push(pos);
        }
        return newFood;
      };

      const startGame = () => {
        const s1 = [{ x: 5, y: 10 }];
        const s2 = [{ x: 25, y: 10 }];
        setSnake1(s1); setSnake2(s2);
        setDirection1({ x: 1, y: 0 }); setDirection2({ x: -1, y: 0 });
        nextDirection1.current = { x: 1, y: 0 };
        nextDirection2.current = { x: -1, y: 0 };
        setFood(generateFood(s1, s2));
        setGameState('playing');
        setWinner('');
      };

      useEffect(() => {
        const onKey = (e) => {
          if (gameState !== 'playing') {
            if (e.key === ' ') startGame();
            return;
          }
          if (e.key === 'w' && direction1.y === 0) nextDirection1.current = { x: 0, y: -1 };
          if (e.key === 's' && direction1.y === 0) nextDirection1.current = { x: 0, y: 1 };
          if (e.key === 'a' && direction1.x === 0) nextDirection1.current = { x: -1, y: 0 };
          if (e.key === 'd' && direction1.x === 0) nextDirection1.current = { x: 1, y: 0 };
          if (e.key === 'ArrowUp' && direction2.y === 0) nextDirection2.current = { x: 0, y: -1 };
          if (e.key === 'ArrowDown' && direction2.y === 0) nextDirection2.current = { x: 0, y: 1 };
          if (e.key === 'ArrowLeft' && direction2.x === 0) nextDirection2.current = { x: -1, y: 0 };
          if (e.key === 'ArrowRight' && direction2.x === 0) nextDirection2.current = { x: 1, y: 0 };
        };
        window.addEventListener('keydown', onKey);
        return () => window.removeEventListener('keydown', onKey);
      }, [gameState, direction1, direction2]);

      useEffect(() => {
        if (gameState !== 'playing') return;

        let prevS1 = snake1;
        let prevS2 = snake2;
        let curFood = food;

        const move = () => {
          setDirection1(nextDirection1.current);
          setDirection2(nextDirection2.current);

          // Snake 1
          const h1 = prevS1[0];
          const nh1 = { x: (h1.x + nextDirection1.current.x + gridSize) % gridSize, y: (h1.y + nextDirection1.current.y + gridSize) % gridSize };
          let ate1 = curFood.findIndex(f => f.x === nh1.x && f.y === nh1.y);
          let ns1 = ate1 !== -1 ? [nh1, ...prevS1] : [nh1, ...prevS1.slice(0, -1)];
          if (ate1 !== -1) curFood = curFood.filter((_, i) => i !== ate1);

          if (ns1.slice(1).some(s => s.x === nh1.x && s.y === nh1.y) || prevS2.some(s => s.x === nh1.x && s.y === nh1.y)) {
            setGameState('gameover'); setWinner('플레이어 2 승리!'); return;
          }

          // Snake 2
          const h2 = prevS2[0];
          const nh2 = { x: (h2.x + nextDirection2.current.x + gridSize) % gridSize, y: (h2.y + nextDirection2.current.y + gridSize) % gridSize };
          let ate2 = curFood.findIndex(f => f.x === nh2.x && f.y === nh2.y);
          let ns2 = ate2 !== -1 ? [nh2, ...prevS2] : [nh2, ...prevS2.slice(0, -1)];
          if (ate2 !== -1) curFood = curFood.filter((_, i) => i !== ate2);

          if (ns2.slice(1).some(s => s.x === nh2.x && s.y === nh2.y) || ns1.some(s => s.x === nh2.x && s.y === nh2.y)) {
            setGameState('gameover'); setWinner('플레이어 1 승리!'); return;
          }

          if (curFood.length < 3) {
            const more = generateFood(ns1, ns2);
            curFood = [...curFood, ...more.slice(0, 3 - curFood.length)];
          }

          prevS1 = ns1; prevS2 = ns2;
          setSnake1(ns1); setSnake2(ns2); setFood(curFood);
        };

        gameLoopRef.current = setInterval(move, 100);
        return () => clearInterval(gameLoopRef.current);
      }, [gameState]);

      const reset = () => setGameState('menu');

      return React.createElement('div', { className: "min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center p-4" },
        React.createElement('div', { className: "max-w-4xl w-full" },
          React.createElement('h1', { className: "text-5xl font-bold text-center mb-8 bg-gradient-to-r from-green-400 via-blue-400 to-purple-400 bg-clip-text text-transparent" }, "Snake Battle"),

          React.createElement('div', { className: "relative bg-slate-800 rounded-2xl p-4 shadow-2xl mb-6" },
            React.createElement('div', { className: "relative bg-black rounded-xl overflow-hidden", style: { width: gridSize * cellSize, height: gridSize * cellSize, margin: '0 auto' } },
              food.map((f, i) => React.createElement('div', { key: `f${i}`, className: "absolute bg-yellow-400 rounded-full animate-pulse", style: { left: f.x * cellSize, top: f.y * cellSize, width: cellSize - 2, height: cellSize - 2, boxShadow: '0 0 10px #facc15' } })),
              snake1.map((s, i) => React.createElement('div', { key: `s1${i}`, className: "absolute rounded-sm", style: { left: s.x * cellSize, top: s.y * cellSize, width: cellSize - 2, height: cellSize - 2, backgroundColor: i === 0 ? '#3b82f6' : '#60a5fa', boxShadow: i === 0 ? '0 0 10px #3b82f6' : 'none' } })),
              snake2.map((s, i) => React.createElement('div', { key: `s2${i}`, className: "absolute rounded-sm", style: { left: s.x * cellSize, top: s.y * cellSize, width: cellSize - 2, height: cellSize - 2, backgroundColor: i === 0 ? '#ef4444' : '#f87171', boxShadow: i === 0 ? '0 0 10px #ef4444' : 'none' } })),
              gameState !== 'playing' && React.createElement('div', { className: "absolute inset-0 bg-black bg-opacity-80 flex flex-col items-center justify-center" },
                gameState === 'menu' ? [
                  React.createElement('div', { key: 't', className: "text-white text-2xl font-bold mb-6" }, "스페이스바로 시작!"),
                  React.createElement('div', { key: 'g', className: "text-gray-300 text-sm space-y-1" }, [
                    React.createElement('div', {}, "Player 1: W A S D"),
                    React.createElement('div', {}, "Player 2: 방향키"),
                    React.createElement('div', {}, "먹이 먹고 성장!"),
                    React.createElement('div', {}, "충돌 시 패배!")
                  ])
                ] : [
                  React.createElement('div', { key: 'w', className: "text-white text-3xl font-bold mb-4" }, winner),
                  React.createElement('div', { key: 'r', className: "text-gray-300 text-lg" }, "스페이스바로 재시작")
                ]
              )
            )
          ),

          React.createElement('div', { className: "flex gap-4 justify-center" }, [
            React.createElement('button', { onClick: startGame, className: "bg-gradient-to-r from-green-500 to-green-600 text-white px-8 py-3 rounded-xl font-bold flex items-center gap-2 shadow-lg" }, React.createElement(Play, { size: 20 }), gameState === 'menu' ? '게임 시작' : '재시작'),
            React.createElement('button', { onClick: reset, className: "bg-gradient-to-r from-gray-600 to-gray-700 text-white px-8 py-3 rounded-xl font-bold flex items-center gap-2 shadow-lg" }, React.createElement(RotateCcw, { size: 20 }), '메뉴')
          ])
        )
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(React.createElement(SnakeBattle));
  </script>
</body>
</html>
"""

st.components.v1.html(HTML_CONTENT, height=800, scrolling=True)

with st.sidebar:
    st.header("조작법")
    st.markdown("""
    - **Player 1**: `W` `A` `S` `D`
    - **Player 2**: `↑` `↓` `←` `→`
    - **시작/재시작**: `Space`
    """)
    st.info("웹 브라우저에서 키보드로 플레이!")
