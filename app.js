const $ = (s) => document.querySelector(s);
const listEl = $('#list');
const titleEl = $('#title');
const countEl = $('#count');
const fileEl = $('#file');
const audio = $('#audio');
const seek = $('#seek');
const tcur = $('#tcur');
const tdur = $('#tdur');
const btnPlay = $('#play');
const btnPrev = $('#prev');
const btnNext = $('#next');
const btnPick = $('#pick');
const btnShuffle = $('#shuffle');
const btnRepeat = $('#repeat');
const vol = $('#vol');

let tracks = []; // {id, name, url}
let index = 0;
let shuffle = false;
let repeatOne = false;

const fmt = (sec) => {
  if (!isFinite(sec)) return '0:00';
  const s = Math.max(0, Math.floor(sec));
  const m = Math.floor(s / 60);
  const r = String(s % 60).padStart(2, '0');
  return `${m}:${r}`;
};

function renderList() {
  countEl.textContent = `(${tracks.length})`;
  listEl.innerHTML = '';
  tracks.forEach((t, i) => {
    const li = document.createElement('li');
    li.className = 'row' + (i === index ? ' active' : '');
    li.innerHTML = `
      <button class="row-btn" data-i="${i}">
        ${i === index ? '▶ ' : ''}${t.name}
      </button>
      <button class="del" data-del="${i}">✕</button>`;
    listEl.appendChild(li);
  });
}

function setTrack(i) {
  if (!tracks[i]) return;
  index = i;
  audio.src = tracks[i].url;
  titleEl.textContent = tracks[i].name;
  renderList();
  if (!audio.paused) audio.play();
}

function next() {
  if (shuffle && tracks.length > 1) {
    let n = index;
    while (n === index) n = Math.floor(Math.random() * tracks.length);
    setTrack(n);
  } else {
    setTrack((index + 1) % tracks.length);
  }
}

function prev() {
  setTrack((index - 1 + tracks.length) % tracks.length);
}

btnPlay.onclick = () => (audio.paused ? audio.play() : audio.pause());
btnNext.onclick = next;
btnPrev.onclick = prev;
btnPick.onclick = () => fileEl.click();
btnShuffle.onclick = () => {
  shuffle = !shuffle;
  btnShuffle.classList.toggle('on', shuffle);
};
btnRepeat.onclick = () => {
  repeatOne = !repeatOne;
  btnRepeat.classList.toggle('on', repeatOne);
};

fileEl.onchange = (e) => addFiles(e.target.files);

function addFiles(fileList) {
  const files = Array.from(fileList).filter((f) => f.type.startsWith('audio'));
  const mapped = files.map((f, i) => ({
