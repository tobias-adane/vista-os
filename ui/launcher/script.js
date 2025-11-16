const hints = [
  'Double tap anywhere to talk',
  'Say "Iris" to wake the assistant',
  'Hold anywhere to enable vision',
  'Single tap to stop Iris'
];
let hintIndex = 0;
const hintText = document.getElementById('hint-text');
setInterval(() => {
  hintIndex = (hintIndex + 1) % hints.length;
  hintText.textContent = hints[hintIndex];
}, 4000);

const statusText = document.getElementById('status-text');
const surface = document.getElementById('surface');
const visionState = document.getElementById('vision-state');
const visionFeed = document.getElementById('vision-feed');
const visionOverlay = document.getElementById('vision-overlay');
const visionEvents = document.getElementById('vision-events');
const commandInput = document.getElementById('command-input');
const runButton = document.getElementById('run-command');
const actionLog = document.getElementById('action-log');

let lastTap = 0;
let holdTimer = null;
let visionInterval = null;

const mockObservations = [
  'Door detected slightly to your right',
  'Clear path ahead for three meters',
  'Curb detected ahead',
  'Person detected two meters ahead',
  'Text detected: EXIT'
];

const mockActions = utterance => {
  const normalized = utterance.toLowerCase();
  if (normalized.includes('message')) {
    return 'Plan → send_message via WhatsApp to Sam: "Te escribo en camino"';
  }
  if (normalized.includes('call') || normalized.includes('llamá')) {
    return 'Plan → make_call to Mom';
  }
  if (normalized.includes('music') || normalized.includes('música')) {
    return 'Plan → play_music on Spotify (liked songs)';
  }
  if (normalized.includes('vision')) {
    return 'Plan → enable vision stream (back camera)';
  }
  return 'Fallback → ask user for clarification';
};

const appendLog = text => {
  const timestamp = new Date().toLocaleTimeString();
  actionLog.textContent = `[${timestamp}] ${text}\n` + actionLog.textContent;
};

const enterListening = () => {
  statusText.textContent = 'Listening…';
  appendLog('Iris is listening');
};

const runUtterance = utterance => {
  if (!utterance.trim()) return;
  statusText.textContent = `Running: "${utterance}"`;
  appendLog(mockActions(utterance));
  commandInput.value = '';
};

const enableVision = () => {
  if (visionFeed.classList.contains('live')) return;
  visionFeed.classList.add('live');
  visionOverlay.textContent = '';
  visionState.textContent = 'Vision active';
  appendLog('Vision mode enabled');
  visionInterval = setInterval(() => {
    const observation = mockObservations[Math.floor(Math.random() * mockObservations.length)];
    const li = document.createElement('li');
    li.textContent = observation;
    visionEvents.prepend(li);
    while (visionEvents.children.length > 4) {
      visionEvents.removeChild(visionEvents.lastChild);
    }
  }, 2500);
};

const disableVision = () => {
  visionFeed.classList.remove('live');
  visionOverlay.textContent = 'Vision paused';
  visionState.textContent = 'Hold anywhere to enable';
  appendLog('Vision mode disabled');
  clearInterval(visionInterval);
  visionInterval = null;
};

surface.addEventListener('click', event => {
  const now = Date.now();
  if (now - lastTap < 400) {
    enterListening();
  } else {
    statusText.textContent = 'Action interrupted';
    appendLog('Single tap → interrupt');
  }
  lastTap = now;
});

surface.addEventListener('pointerdown', () => {
  holdTimer = setTimeout(() => {
    enableVision();
  }, 700);
});

surface.addEventListener('pointerup', () => {
  clearTimeout(holdTimer);
  holdTimer = null;
  if (visionFeed.classList.contains('live')) {
    disableVision();
  }
});

runButton.addEventListener('click', () => runUtterance(commandInput.value));
commandInput.addEventListener('keydown', event => {
  if (event.key === 'Enter') {
    runUtterance(commandInput.value);
  }
});
