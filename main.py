import React, { useState, useEffect, useRef } from 'react';
import { Play, RotateCcw, Trophy } from 'lucide-react';

export default function SnakeBattle() {
  const [gameState, setGameState] = useState('menu'); // menu, playing, gameover
  const [snake1, setSnake1] = useState([{ x: 5, y: 10 }]);
  const [snake2, setSnake2] = useState([{ x: 25, y: 10 }]);
  const [direction1, setDirection1] = useState({ x: 1, y: 0 });
  const [direction2, setDirection2] = useState({ x: -1, y: 0 });
  const [food, setFood] = useState([]);
  const [scores, setScores] = useState({ player1: 0, player2: 0 });
  const [winner, setWinner] = useState('');
  const [snakeLength, setSnakeLength] = useState(1);
  const [roundTime, setRoundTime] = useState(0);
  const [gameWinner, setGameWinner] = useState(null);
  const snakeLengthRef = useRef(1);
  const gameStartTimeRef = useRef(null);
  
  const gridSize = 20;
  const cellSize = 20;
  const gameLoopRef = useRef(null);
  const nextDirection1 = useRef({ x: 1, y: 0 });
  const nextDirection2 = useRef({ x: -1, y: 0 });

  // 먹이 생성
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

  // 게임 시작
  const startGame = () => {
    if (gameWinner) {
      setScores({ player1: 0, player2: 0 });
      setGameWinner(null);
    }
    
    const initialSnake1 = [{ x: 3, y: 10 }];
    const initialSnake2 = [{ x: 16, y: 10 }];
    
    setSnake1(initialSnake1);
    setSnake2(initialSnake2);
    setDirection1({ x: 1, y: 0 });
    setDirection2({ x: -1, y: 0 });
    nextDirection1.current = { x: 1, y: 0 };
    nextDirection2.current = { x: -1, y: 0 };
    setFood(generateFood(initialSnake1, initialSnake2));
    setGameState('playing');
    setWinner('');
    setSnakeLength(1);
    snakeLengthRef.current = 1;
    gameStartTimeRef.current = Date.now();
    setRoundTime(0);
  };

  // 키보드 입력
  useEffect(() => {
    const handleKeyPress = (e) => {
      if (gameState !== 'playing') {
        if (e.key === ' ') {
          startGame();
        }
        return;
      }

      // Player 1: WASD
      if (e.key === 'w' && direction1.y === 0) {
        nextDirection1.current = { x: 0, y: -1 };
      } else if (e.key === 's' && direction1.y === 0) {
        nextDirection1.current = { x: 0, y: 1 };
      } else if (e.key === 'a' && direction1.x === 0) {
        nextDirection1.current = { x: -1, y: 0 };
      } else if (e.key === 'd' && direction1.x === 0) {
        nextDirection1.current = { x: 1, y: 0 };
      }

      // Player 2: Arrow Keys
      if (e.key === 'ArrowUp' && direction2.y === 0) {
        nextDirection2.current = { x: 0, y: -1 };
      } else if (e.key === 'ArrowDown' && direction2.y === 0) {
        nextDirection2.current = { x: 0, y: 1 };
      } else if (e.key === 'ArrowLeft' && direction2.x === 0) {
        nextDirection2.current = { x: -1, y: 0 };
      } else if (e.key === 'ArrowRight' && direction2.x === 0) {
        nextDirection2.current = { x: 1, y: 0 };
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [gameState, direction1, direction2]);

  // 게임 루프
  useEffect(() => {
    if (gameState !== 'playing') return;

    // 라운드 시간 증가 타이머 (1초마다)
    const timeInterval = setInterval(() => {
      setRoundTime(prev => prev + 1);
    }, 1000);

    gameLoopRef.current = setInterval(() => {
      // 현재 시간 기반으로 뱀 길이 계산 (2초마다 1칸)
      const elapsedSeconds = Math.floor((Date.now() - gameStartTimeRef.current) / 1000);
      const currentLength = Math.floor(elapsedSeconds / 2) + 1;
      snakeLengthRef.current = currentLength;
      setSnakeLength(currentLength);

      setDirection1(nextDirection1.current);
      setDirection2(nextDirection2.current);

      setSnake1(prev => {
        const head = prev[0];
        const newHead = {
          x: (head.x + nextDirection1.current.x + gridSize) % gridSize,
          y: (head.y + nextDirection1.current.y + gridSize) % gridSize
        };

        // 새로운 뱀 몸통 생성
        const newSnake = [newHead, ...prev];
        
        // 먹이 먹기 체크
        const ateFood = food.findIndex(f => f.x === newHead.x && f.y === newHead.y);
        
        if (ateFood !== -1) {
          setScores(s => {
            const newScore = { ...s, player1: s.player1 + 10 };
            if (newScore.player1 >= 500) {
              setGameState('gameover');
              setGameWinner('player1');
              setWinner('🎉 플레이어 1 최종 승리! 🎉');
            }
            return newScore;
          });
          setFood(f => {
            const newFood = [...f];
            newFood.splice(ateFood, 1);
            if (newFood.length < 3) {
              const additionalFood = generateFood(newSnake, snake2);
              return [...newFood, ...additionalFood.slice(0, 3 - newFood.length)];
            }
            return newFood;
          });
        }

        // 시간에 따른 길이로 제한
        return newSnake.slice(0, currentLength);
      });

      setSnake2(prev => {
        const head = prev[0];
        const newHead = {
          x: (head.x + nextDirection2.current.x + gridSize) % gridSize,
          y: (head.y + nextDirection2.current.y + gridSize) % gridSize
        };

        // 새로운 뱀 몸통 생성
        const newSnake = [newHead, ...prev];
        
        // 먹이 먹기 체크
        const ateFood = food.findIndex(f => f.x === newHead.x && f.y === newHead.y);
        
        if (ateFood !== -1) {
          setScores(s => {
            const newScore = { ...s, player2: s.player2 + 10 };
            if (newScore.player2 >= 500) {
              setGameState('gameover');
              setGameWinner('player2');
              setWinner('🎉 플레이어 2 최종 승리! 🎉');
            }
            return newScore;
          });
          setFood(f => {
            const newFood = [...f];
            newFood.splice(ateFood, 1);
            if (newFood.length < 3) {
              const additionalFood = generateFood(snake1, newSnake);
              return [...newFood, ...additionalFood.slice(0, 3 - newFood.length)];
            }
            return newFood;
          });
        }

        // 시간에 따른 길이로 제한
        return newSnake.slice(0, currentLength);
      });

      // 충돌 체크
      setSnake1(s1 => {
        setSnake2(s2 => {
          const head1 = s1[0];
          const head2 = s2[0];

          const p1HitSelf = s1.slice(1).some(s => s.x === head1.x && s.y === head1.y);
          const p1HitP2 = s2.some(s => s.x === head1.x && s.y === head1.y);
          const p2HitSelf = s2.slice(1).some(s => s.x === head2.x && s.y === head2.y);
          const p2HitP1 = s1.some(s => s.x === head2.x && s.y === head2.y);

          // 킬 보너스 = 50 + (라운드 시간 * 2)
          const killBonus = 50 + (roundTime * 2);

          if (p1HitSelf || p1HitP2) {
            setScores(s => {
              const newScore = { ...s, player2: s.player2 + killBonus };
              if (newScore.player2 >= 500) {
                setGameWinner('player2');
                setWinner('🎉 플레이어 2 최종 승리! 🎉');
              } else {
                setWinner(`플레이어 2 라운드 승리! +${killBonus}점`);
              }
              return newScore;
            });
            setGameState('gameover');
          } else if (p2HitSelf || p2HitP1) {
            setScores(s => {
              const newScore = { ...s, player1: s.player1 + killBonus };
              if (newScore.player1 >= 500) {
                setGameWinner('player1');
                setWinner('🎉 플레이어 1 최종 승리! 🎉');
              } else {
                setWinner(`플레이어 1 라운드 승리! +${killBonus}점`);
              }
              return newScore;
            });
            setGameState('gameover');
          }

          return s2;
        });
        return s1;
      });
    }, 100);

    return () => {
      if (gameLoopRef.current) {
        clearInterval(gameLoopRef.current);
      }
      clearInterval(timeInterval);
    };
  }, [gameState, food]);

  const resetGame = () => {
    setScores({ player1: 0, player2: 0 });
    setGameState('menu');
    setGameWinner(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center p-4">
      <div className="max-w-4xl w-full">
        <h1 className="text-5xl font-bold text-center mb-6 bg-gradient-to-r from-green-400 via-blue-400 to-purple-400 bg-clip-text text-transparent">
          🐍 스네이크 배틀 🐍
        </h1>

        {/* 점수판 */}
        <div className="grid grid-cols-2 gap-4 mb-6">
          <div className="bg-gradient-to-br from-blue-500 to-blue-700 rounded-2xl p-4 text-center shadow-xl">
            <div className="text-white text-sm font-semibold mb-1">플레이어 1 (WASD)</div>
            <div className="text-4xl font-bold text-white">{scores.player1}</div>
            <div className="text-xs text-blue-200 mt-1">목표: 500점</div>
          </div>
          <div className="bg-gradient-to-br from-red-500 to-red-700 rounded-2xl p-4 text-center shadow-xl">
            <div className="text-white text-sm font-semibold mb-1">플레이어 2 (방향키)</div>
            <div className="text-4xl font-bold text-white">{scores.player2}</div>
            <div className="text-xs text-red-200 mt-1">목표: 500점</div>
          </div>
        </div>

        {/* 게임 보드 */}
        <div className="relative bg-slate-800 rounded-2xl p-4 shadow-2xl mb-4">
          {gameState === 'playing' && (
            <div className="text-center mb-2 space-y-1">
              <span className="text-white text-sm block">
                라운드 시간: {roundTime}초 | 킬 보너스: {50 + (roundTime * 2)}점
              </span>
              <span className="text-yellow-300 text-xs block">
                뱀 길이: {snakeLength} | P1 실제: {snake1.length} | P2 실제: {snake2.length}
              </span>
            </div>
          )}
          <div 
            className="relative bg-black rounded-xl overflow-hidden"
            style={{ 
              width: gridSize * cellSize, 
              height: gridSize * cellSize,
              margin: '0 auto'
            }}
          >
            {/* 먹이 */}
            {food.map((f, i) => (
              <div
                key={`food-${i}`}
                className="absolute bg-yellow-400 rounded-full animate-pulse"
                style={{
                  left: f.x * cellSize,
                  top: f.y * cellSize,
                  width: cellSize - 3,
                  height: cellSize - 3,
                  boxShadow: '0 0 15px rgba(250, 204, 21, 0.8)'
                }}
              />
            ))}

            {/* Snake 1 */}
            {snake1.map((segment, i) => (
              <div
                key={`s1-${i}`}
                className="absolute rounded"
                style={{
                  left: segment.x * cellSize,
                  top: segment.y * cellSize,
                  width: cellSize - 3,
                  height: cellSize - 3,
                  backgroundColor: i === 0 ? '#3b82f6' : '#60a5fa',
                  boxShadow: i === 0 ? '0 0 15px rgba(59, 130, 246, 0.8)' : 'none'
                }}
              />
            ))}

            {/* Snake 2 */}
            {snake2.map((segment, i) => (
              <div
                key={`s2-${i}`}
                className="absolute rounded"
                style={{
                  left: segment.x * cellSize,
                  top: segment.y * cellSize,
                  width: cellSize - 3,
                  height: cellSize - 3,
                  backgroundColor: i === 0 ? '#ef4444' : '#f87171',
                  boxShadow: i === 0 ? '0 0 15px rgba(239, 68, 68, 0.8)' : 'none'
                }}
              />
            ))}

            {/* 게임 오버레이 */}
            {gameState !== 'playing' && (
              <div className="absolute inset-0 bg-black bg-opacity-80 flex flex-col items-center justify-center">
                {gameState === 'menu' ? (
                  <>
                    <div className="text-white text-2xl font-bold mb-6 text-center">
                      스페이스바를 눌러 시작!
                    </div>
                    <div className="text-gray-300 text-sm text-center space-y-2">
                      <div>🔵 플레이어 1: W/A/S/D 키</div>
                      <div>🔴 플레이어 2: 방향키</div>
                      <div>🏆 먼저 500점에 도달하면 승리!</div>
                      <div>⏱️ 뱀은 2초마다 자동으로 길어집니다</div>
                      <div>⭐ 먹이: +10점</div>
                      <div>💥 킬: 50 + (시간 × 2)점</div>
                    </div>
                  </>
                ) : (
                  <>
                    <div className="text-white text-3xl font-bold mb-4">
                      {winner}
                    </div>
                    <div className="text-gray-300 text-lg mb-6">
                      스페이스바로 다시 시작
                    </div>
                  </>
                )}
              </div>
            )}
          </div>
        </div>

        {/* 버튼 */}
        <div className="flex gap-4 justify-center">
          <button
            onClick={startGame}
            className="bg-gradient-to-r from-green-500 to-green-600 text-white px-8 py-3 rounded-xl font-bold hover:from-green-600 hover:to-green-700 transition-all shadow-lg flex items-center gap-2"
          >
            <Play size={20} />
            {gameWinner ? '새 게임' : gameState === 'menu' ? '게임 시작' : '다음 라운드'}
          </button>
          <button
            onClick={resetGame}
            className="bg-gradient-to-r from-gray-600 to-gray-700 text-white px-8 py-3 rounded-xl font-bold hover:from-gray-700 hover:to-gray-800 transition-all shadow-lg flex items-center gap-2"
          >
            <RotateCcw size={20} />
            점수 초기화
          </button>
        </div>
      </div>
    </div>
  );
}
