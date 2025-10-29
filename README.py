# main.py
import streamlit as st

st.set_page_config(
    page_title="Snake Battle",
    page_icon="snake",
    layout="centered"
)

# -------------------------------
# 1. React 빌드 없이 인라인 HTML + JS + CSS 삽입
# -------------------------------
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Snake Battle</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body { margin: 0; padding: 0; background: #0f172a; }
    #game-container { max-width: 600px; margin: 0 auto; padding: 1rem; }
  </style>
</head>
<body>
  <div id="root"></div>

  <script type="module">
    import React from "https://esm.sh/react@18";
    import ReactDOM from "https://esm.sh/react-dom@18";
    import { Play, RotateCcw, Trophy } from "https://esm.sh/lucide-react@0.263";

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

      const generateFood = (snake1Pos, snake2Pos) => {
        const newFood = [];
        for (let i = 0; i < 3; i++) {
          let foodPos;
          let attempts = 0;
          do {
            foodPos = {
              x: Math.floor(Math.random() * gridSize),
              y: Math.floor(Math.random() * gridSize)
            };
            attempts++;
          } while (
            attempts < 100 &&
            (snake1Pos.some(s => s.x === foodPos.x && s.y === foodPos.y) ||
             snake2Pos.some(s => s.x === foodPos.x && s.y === foodPos.y) ||
             newFood.some(f => f.x === foodPos.x && f.y === foodPos.y))
          );
          newFood.push(foodPos);
        }
        return newFood;
      };

      const startGame = () => {
        const initialSnake1 = [{ x: 5, y: 10 }];
        const initialSnake2 = [{ x: 25, y: 10 }];
        setSnake1(initialSnake1);
        setSnake2(initialSnake2);
        setDirection1({ x: 1, y: 0 });
        setDirection2({ x: -1, y: 0 });
        nextDirection1.current = { x: 1, y: 0 };
        nextDirection2.current = { x: -1, y: 0 };
        setFood(generateFood(initialSnake1, initialSnake2));
        setGameState('playing');
        setWinner('');
      };

      useEffect(() => {
        const handleKeyPress = (e) => {
          if (gameState !== 'playing') {
            if (e.key === ' ') startGame();
            return;
          }
          // Player 1: WASD
          if (e.key === 'w' && direction1.y === 0) nextDirection1.current = { x: 0, y: -1 };
          else if (e.key === 's' && direction1.y === 0) nextDirection1.current = { x: 0, y: 1 };
          else if (e.key === 'a' && direction1.x === 0) nextDirection1.current = { x: -1, y: 0 };
          else if (e.key === 'd' && direction1.x === 0) nextDirection1.current = { x: 1, y: 0 };

          // Player 2: Arrow Keys
          if (e.key === 'ArrowUp' && direction2.y === 0) nextDirection2.current = { x: 0, y: -1 };
          else if (e.key === 'ArrowDown' && direction2.y === 0) nextDirection2.current = { x: 0, y: 1 };
          else if (e.key === 'ArrowLeft' && direction2.x === 0) nextDirection2.current = { x: -1, y: 0 };
          else if (e.key === 'ArrowRight' && direction2.x === 0) nextDirection2.current = { x: 1, y: 0 };
        };
        window.addEventListener('keydown', handleKeyPress);
        return () => window.removeEventListener('keydown', handleKeyPress);
      }, [gameState, direction1, direction2]);

      useEffect(() => {
        if (gameState !== 'playing') return;

        // 상태를 한 번에 업데이트하기 위해 prev 상태 캡처
        let prevSnake1 = snake1;
        let prevSnake2 = snake2;
        let currentFood = food;

        const moveSnake = () => {
          setDirection1(nextDirection1.current);
          setDirection2(nextDirection2.current);

          // Snake 1 이동
          const head1 = prevSnake1[0];
          const newHead1 = {
            x: (head1.x + nextDirection1.current.x + gridSize) % gridSize,
            y: (head1.y + nextDirection1.current.y + gridSize) % gridSize
          };

          let ateFood1 = currentFood.findIndex(f => f.x === newHead1.x && f.y === newHead1.y);
          let newSnake1 = ateFood1 !== -1 ? [newHead1, ...prevSnake1] : [newHead1, ...prevSnake1.slice(0, -1)];

          if (ateFood1 !== -1) {
            currentFood = currentFood.filter((_, i) => i !== ateFood1);
          }

          // 충돌 체크 (자기 몸 or 상대)
          if (
            newSnake1.slice(1).some(s => s.x === newHead1.x && s.y === newHead1.y) ||
            prevSnake2.some(s => s.x === newHead1.x && s.y === newHead1.y)
          ) {
            setGameState('gameover');
            setWinner('플레이어 2 승리! Trophy');
            return;
          }

          // Snake 2 이동
          const head2 = prevSnake2[0];
          const newHead2 = {
            x: (head2.x + nextDirection2.current.x + gridSize) % gridSize,
            y: (head2.y + nextDirection2.current.y + gridSize) % gridSize
          };

          let ateFood2 = currentFood.findIndex(f => f.x === newHead2.x && f.y === newHead2.y);
          let newSnake2 = ateFood2 !== -1 ? [newHead2, ...prevSnake2] : [newHead2, ...prevSnake2.slice(0, -1)];

          if (ateFood2 !== -1) {
            currentFood = currentFood.filter((_, i) => i !== ateFood2);
          }

          if (
            newSnake2.slice(1).some(s => s.x === newHead2.x && s.y === newHead2.y) ||
            newSnake1.some(s => s.x === newHead2.x && s.y === newHead2.y)
          ) {
            setGameState('gameover');
            setWinner('플레이어 1 승리! Trophy');
            return;
          }

          // 먹이 보충
          if (currentFood.length < 3) {
            const additional = generateFood(newSnake1, newSnake2);
            currentFood = [...currentFood, ...additional.slice(0, 3 - currentFood.length)];
          }

          prevSnake1 = newSnake1;
          prevSnake2 = newSnake2;
          setSnake1(newSnake1);
          setSnake2(newSnake2);
          setFood(currentFood);
        };

        gameLoopRef.current = setInterval(moveSnake, 100);
        return () => clearInterval(gameLoopRef.current);
      }, [gameState]);

      const resetGame = () => setGameState('menu');

      return React.createElement('div', { className: "min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center p-4" },
        React.createElement('div', { className: "max-w-4xl w-full" },
          React.createElement('h1', {
            className: "text-5xl font-bold text-center mb-8 bg-gradient-to-r from-green-400 via-blue-400 to-purple-400 bg-clip-text text-transparent"
          }, "Snake Battle Snake Battle"),

          // 게임 보드
          React.createElement('div', { className: "relative bg-slate-800 rounded-2xl p-4 shadow-2xl mb-6" },
            React.createElement('div', {
              className: "relative bg-black rounded-xl overflow-hidden",
              style: { width: gridSize * cellSize, height: gridSize * cellSize, margin: '0 auto' }
            },
              // 먹이
              food.map((f, i) => React.createElement('div', {
                key: `food-${i}`,
                className: "absolute bg-yellow-400 rounded-full animate-pulse",
                style: {
                  left: f.x * cellSize,
                  top: f.y * cellSize,
                  width: cellSize - 2,
                  height: cellSize - 2,
                  boxShadow: '0 0 10px rgba(250, 204, 21, 0.8)'
                }
              })),

              // Snake 1
              snake1.map((s, i) => React.createElement('div', {
                key: `s1-${i}`,
                className: "absolute rounded-sm",
                style: {
                  left: s.x * cellSize,
                  top: s.y * cellSize,
                  width: cellSize - 2,
                  height: cellSize - 2,
                  backgroundColor: i === 0 ? '#3b82f6' : '#60a5fa',
                  boxShadow: i === 0 ? '0 0 10px rgba(59, 130, 246, 0.8)' : 'none'
                }
              })),

              // Snake 2
              snake2.map((s, i) => React.createElement('div', {
                key: `s2-${i}`,
                className: "absolute rounded-sm",
                style: {
                  left: s.x * cellSize,
                  top: s.y * cellSize,
                  width: cellSize - 2,
                  height: cellSize - 2,
                  backgroundColor: i === 0 ? '#ef4444' : '#f87171',
                  boxShadow: i === 0 ? '0 0 10px rgba(239, 68, 68, 0.8)' : 'none'
                }
              })),

              // 오버레이
              gameState !== 'playing' && React.createElement('div', {
                className: "absolute inset-0 bg-black bg-opacity-80 flex flex-col items-center justify-center"
              },
                gameState === 'menu' ? [
                  React.createElement('div', { key: 'title', className: "text-white text-2xl font-bold mb-6 text-center" }, "스페이스바를 눌러 시작!"),
                  React.createElement('div', { key: 'guide', className: "text-gray-300 text-sm text-center space-y-2" }, [
                    React.createElement('div', { key: 'p1' }, "Player 1: W/A/S/D 키"),
                    React.createElement('div', { key: 'p2' }, "Player 2: 방향키"),
                    React.createElement('div', { key: 'eat' }, "먹이를 먹고 점수를 얻으세요!"),
                    React.createElement('div', { key: 'crash' }, "자신이나 상대와 부딪히면 패배!")
                  ])
                ] : [
                  React.createElement('div', { key: 'win', className: "text-white text-3xl font-bold mb-4" }, winner),
                  React.createElement('div', { key: 'restart', className: "text-gray-300 text-lg mb-6" }, "스페이스바로 다시 시작")
                ]
              )
            )
          ),

          // 버튼
          React.createElement('div', { className: "flex gap-4 justify-center" }, [
            React.createElement('button', {
              key: 'start',
              onClick: startGame,
              className: "bg-gradient-to-r from-green-500 to-green-600 text-white px-8 py-3 rounded-xl font-bold hover:from-green-600 hover:to-green-700 transition-all shadow-lg flex items-center gap-2"
            }, React.createElement(Play, { size: 20 }), gameState === 'menu' ? '게임 시작' : '다시 시작'),
            React.createElement('button', {
              key: 'menu',
              onClick: resetGame,
              className: "bg-gradient-to-r from-gray-600 to-gray-700 text-white px-8 py-3 rounded-xl font-bold hover:from-gray-700 hover:to-gray-800 transition-all shadow-lg flex items-center gap-2"
            }, React.createElement(RotateCcw, { size: 20 }), '메뉴로')
          ])
        )
      );
    }

    ReactDOM.createRoot(document.getElementById('root')).render(React.createElement(SnakeBattle));
  </script>
</body>
</html>
"""

# -------------------------------
# 2. Streamlit에 삽입
# -------------------------------
st.components.v1.html(
    HTML_CONTENT,
    height=800,
    scrolling=True
)

# -------------------------------
# 3. 사이드바 설명
# -------------------------------
with st.sidebar:
    st.header("조작법")
    st.markdown("""
    - **Player 1**: `W` `A` `S` `D`
    - **Player 2**: `↑` `↓` `←` `→`
    - **시작/재시작**: `Space`
    """)
    st.info("두 뱀이 동시에 움직이며, 먹이를 먹으면 길이가 늘어납니다!")
