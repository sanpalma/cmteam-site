const screens = {
  start: document.getElementById('start-screen'),
  game: document.getElementById('game-screen'),
  result: document.getElementById('result-screen'),
};

const startBtn = document.getElementById('start-btn');
const restartBtn = document.getElementById('restart-btn');
const zoneLabel = document.getElementById('zone-label');
const timeLabel = document.getElementById('time-label');
const energyLabel = document.getElementById('energy-value');
const energyBar = document.getElementById('energy-bar');
const summary = document.getElementById('result-summary');

const canvas = document.getElementById('game-canvas');
const ctx = canvas.getContext('2d');

const zones = {
  A0: { drain: 0.5, key: '1' },
  A1: { drain: 1, key: '2' },
  A2: { drain: 2, key: '3' },
  A3: { drain: 4, key: '4' },
  Vo2: { drain: 6, key: '5' },
};

const map = {
  walls: [
    { x: 120, y: 80, w: 20, h: 300 },
    { x: 260, y: 0, w: 20, h: 260 },
    { x: 260, y: 320, w: 20, h: 200 },
    { x: 420, y: 80, w: 20, h: 350 },
    { x: 580, y: 0, w: 20, h: 260 },
    { x: 580, y: 320, w: 20, h: 200 },
    { x: 740, y: 80, w: 20, h: 300 },
    { x: 120, y: 80, w: 640, h: 20 },
    { x: 120, y: 360, w: 640, h: 20 },
  ],
  goal: { x: 820, y: 460, r: 16 },
};

let state;
let raf;

function initState() {
  const energyBoxes = [
    { x: 80, y: 80, r: 7, taken: false },
    { x: 210, y: 270, r: 7, taken: false },
    { x: 350, y: 450, r: 7, taken: false },
    { x: 510, y: 140, r: 7, taken: false },
    { x: 680, y: 440, r: 7, taken: false },
    { x: 810, y: 80, r: 7, taken: false },
  ];

  state = {
    running: true,
    won: false,
    startTime: performance.now(),
    elapsed: 0,
    energy: 100,
    zone: 'A0',
    zoneTimes: { A0: 0, A1: 0, A2: 0, A3: 0, Vo2: 0 },
    highIntensityTime: 0,
    player: { x: 38, y: 38, r: 12, speed: 180, vx: 0, vy: 0 },
    keys: { ArrowUp: false, ArrowDown: false, ArrowLeft: false, ArrowRight: false },
    energyBoxes,
    villain: {
      active: false,
      x: 840,
      y: 40,
      r: 12,
      speed: 150,
    },
    message: '',
  };
}

function showScreen(name) {
  Object.values(screens).forEach((screen) => screen.classList.remove('active'));
  screens[name].classList.add('active');
}

function startGame() {
  initState();
  showScreen('game');
  cancelAnimationFrame(raf);
  loop(performance.now());
}

function endGame(won, reason = '') {
  state.running = false;
  state.won = won;
  state.message = reason;
  cancelAnimationFrame(raf);
  renderResult();
  showScreen('result');
}

function formatZoneDistribution() {
  return Object.keys(state.zoneTimes)
    .map((zone) => `<li>${zone}: ${state.zoneTimes[zone].toFixed(1)}s</li>`)
    .join('');
}

function behaviorMessage() {
  const high = state.zoneTimes.A3 + state.zoneTimes.Vo2;
  if (!state.won) return 'The Wall won this round. Respect your limits and try again.';
  if (high > state.elapsed * 0.45) return 'Strong effort, but pacing too aggressive. bePatient.';
  if (state.energy > 55) return 'Excellent balance. beHumble and keep the flow.';
  return 'Solid finish. beStrong and refine your zone control.';
}

function renderResult() {
  summary.innerHTML = `
    <p><strong>Final time:</strong> ${state.elapsed.toFixed(1)}s</p>
    <p><strong>Energy left:</strong> ${Math.max(0, state.energy).toFixed(1)}%</p>
    <p><strong>Result:</strong> ${state.won ? 'Victory' : 'Game Over'}${state.message ? ` — ${state.message}` : ''}</p>
    <p><strong>Zone distribution:</strong></p>
    <ul>${formatZoneDistribution()}</ul>
    <p><em>${behaviorMessage()}</em></p>
  `;
}

function updateHUD() {
  zoneLabel.textContent = state.zone;
  timeLabel.textContent = `${state.elapsed.toFixed(1)}s`;
  energyLabel.textContent = `${Math.max(0, state.energy).toFixed(1)}%`;
  energyBar.style.width = `${Math.max(0, Math.min(100, state.energy))}%`;
}

function collidesWall(x, y, r) {
  for (const wall of map.walls) {
    const closestX = Math.max(wall.x, Math.min(x, wall.x + wall.w));
    const closestY = Math.max(wall.y, Math.min(y, wall.y + wall.h));
    const dx = x - closestX;
    const dy = y - closestY;
    if (dx * dx + dy * dy < r * r) return true;
  }
  return x - r < 0 || x + r > canvas.width || y - r < 0 || y + r > canvas.height;
}

function updatePlayer(dt) {
  const { player, keys } = state;
  let dx = 0;
  let dy = 0;
  if (keys.ArrowLeft) dx -= 1;
  if (keys.ArrowRight) dx += 1;
  if (keys.ArrowUp) dy -= 1;
  if (keys.ArrowDown) dy += 1;

  const mag = Math.hypot(dx, dy) || 1;
  player.vx = (dx / mag) * player.speed;
  player.vy = (dy / mag) * player.speed;

  const nextX = player.x + player.vx * dt;
  if (!collidesWall(nextX, player.y, player.r)) player.x = nextX;
  const nextY = player.y + player.vy * dt;
  if (!collidesWall(player.x, nextY, player.r)) player.y = nextY;
}

function updateEnergy(dt) {
  state.zoneTimes[state.zone] += dt;
  state.energy -= zones[state.zone].drain * dt;
  if (state.zone === 'A3' || state.zone === 'Vo2') {
    state.highIntensityTime += dt;
    if (state.highIntensityTime > 5) state.villain.active = true;
  } else {
    state.highIntensityTime = 0;
  }

  for (const box of state.energyBoxes) {
    if (box.taken) continue;
    const d = Math.hypot(state.player.x - box.x, state.player.y - box.y);
    if (d <= state.player.r + box.r + 1) {
      box.taken = true;
      state.energy = Math.min(100, state.energy + 10);
    }
  }

  if (state.energy <= 0) endGame(false, 'Out of energy');
}

function updateVillain(dt) {
  const v = state.villain;
  if (!v.active) return;
  const angle = Math.atan2(state.player.y - v.y, state.player.x - v.x);
  const nx = v.x + Math.cos(angle) * v.speed * dt;
  const ny = v.y + Math.sin(angle) * v.speed * dt;

  if (!collidesWall(nx, v.y, v.r)) v.x = nx;
  if (!collidesWall(v.x, ny, v.r)) v.y = ny;

  const distance = Math.hypot(state.player.x - v.x, state.player.y - v.y);
  if (distance <= state.player.r + v.r) endGame(false, 'Caught by Ego Pace');
}

function checkGoal() {
  const d = Math.hypot(state.player.x - map.goal.x, state.player.y - map.goal.y);
  if (d <= state.player.r + map.goal.r) endGame(true);
}

function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  ctx.fillStyle = '#2a2a2a';
  map.walls.forEach((w) => ctx.fillRect(w.x, w.y, w.w, w.h));

  ctx.fillStyle = '#38f092';
  ctx.beginPath();
  ctx.arc(map.goal.x, map.goal.y, map.goal.r, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = '#ffd633';
  state.energyBoxes.forEach((box) => {
    if (box.taken) return;
    ctx.beginPath();
    ctx.arc(box.x, box.y, box.r, 0, Math.PI * 2);
    ctx.fill();
  });

  ctx.fillStyle = '#4b83ff';
  ctx.beginPath();
  ctx.arc(state.player.x, state.player.y, state.player.r, 0, Math.PI * 2);
  ctx.fill();

  if (state.villain.active) {
    ctx.fillStyle = '#ff4747';
    ctx.beginPath();
    ctx.arc(state.villain.x, state.villain.y, state.villain.r, 0, Math.PI * 2);
    ctx.fill();
  }
}

function loop(ts) {
  if (!state.running) return;
  const dt = Math.min(0.035, (ts - (state.lastTick || ts)) / 1000);
  state.lastTick = ts;
  state.elapsed = (ts - state.startTime) / 1000;

  updatePlayer(dt);
  updateEnergy(dt);
  updateVillain(dt);
  checkGoal();
  updateHUD();
  draw();

  if (state.running) raf = requestAnimationFrame(loop);
}

window.addEventListener('keydown', (event) => {
  if (state && event.key in state.keys) {
    state.keys[event.key] = true;
    event.preventDefault();
  }
  const selected = Object.entries(zones).find(([, cfg]) => cfg.key === event.key);
  if (selected && state?.running) state.zone = selected[0];
});

window.addEventListener('keyup', (event) => {
  if (state && event.key in state.keys) {
    state.keys[event.key] = false;
    event.preventDefault();
  }
});

startBtn.addEventListener('click', startGame);
restartBtn.addEventListener('click', startGame);

showScreen('start');
