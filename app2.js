const $ = (s) => document.querySelector(s);
const listEl = $('#list'), titleEl = $('#title'), countEl = $('#count');
const fileEl = $('#file'), audio = $('#audio'), seek = $('#seek');
const tcur = $('#tcur'), tdur = $('#tdur');
const btnPlay = $('#play'), btnPrev = $('#prev'), btnNext = $('#next');
const btnPick = $('#pick'), btnPick2 = $('#pick2');
const btnShuffle = $('#shuffle'), btnRepeat = $('#repeat');
const vol = $('#vol');

let tracks = [], index = 0, shuffle = false, repeatOne = false;

const fmt = (sec) => { if (!isFinite(sec)) return '0:00';
  const s = Math.max(0, Math.floor(sec)), m = Math.floor(s/60), r = String(s%60).padStart(2,'0'); return `${m}:${r}`; };

function renderList() {
  countEl.textContent = `(${tracks.length})`;
  listEl.innerHTML = '';
  tracks.forEach((t, i) => {
    const li = document.createElement('li');
    li.className = 'row' + (i === index ? ' active' : '');
    li.innerHTML = `<button class="row-btn" data-i="${i}">${i===index?'▶ ':''}${t.name}</button><button class="del" data-del="${i}">✕</button>`;
    listEl.appendChild(li);
  });
}

function setTrack(i) { if (!tracks[i]) return;
  index = i; audio.src = tracks[i].url; titleEl.textContent = tracks[i].name; renderList(); if (!audio.paused) audio.play(); }

function next() {
  if (shuffle && tracks.length > 1) { let n = index; while (n === index) n = Math.floor(Math.random()*tracks.length); setTrack(n); }
  else setTrack((index+1)%tracks.length);
}
function prev() { setTrack((index - 1 + tracks.length) % tracks.length); }

btnPlay.onclick = () => (audio.paused ? audio.play() : audio.pause());
btnNext.onclick = next; btnPrev.onclick = prev;
btnShuffle.onclick = () => { shuffle = !shuffle; btnShuffle.classList.toggle('on', shuffle); };
btnRepeat.onclick   = () => { repeatOne = !repeatOne; btnRepeat.classList.toggle('on', repeatOne); };
vol.oninput  = (e) => (audio.volume = parseFloat(e.target.value));
seek.oninput = (e) => (audio.currentTime = parseFloat(e.target.value));

listEl.onclick = (e) => {
  const i = e.target.getAttribute('data-i'); if (i !== null) setTrack(parseInt(i));
  const del = e.target.getAttribute('data-del'); if (del !== null) {
    const di = parseInt(del); tracks.splice(di,1);
    if (!tracks.length) { audio.pause(); audio.removeAttribute('src'); titleEl.textContent = '—'; }
    else if (di === index) { index = Math.min(index, tracks.length-1); setTrack(index); }
    renderList();
  }
};

audio.onplay = () => (btnPlay.textContent = '⏸');
audio.onpause = () => (btnPlay.textContent = '▶');
audio.ontimeupdate = () => { seek.max = audio.duration || 0; seek.value = audio.currentTime; tcur.textContent = fmt(audio.currentTime); tdur.textContent = fmt(audio.duration); };
audio.onended = () => { if (repeatOne) { audio.currentTime = 0; audio.play(); } else next(); };

// ---- Import classique (input) ----
fileEl.onchange = (e) => addFileList(e.target.files);
$('#pick').onclick = () => fileEl.click();

// ---- Import mode 2 (File System Access API) ----
$('#pick2').onclick = async () => {
  if (!window.showOpenFilePicker) {
    alert("Mode 2 non supporté par ce navigateur. Essaie 'Importer (classique)'.");
    return;
  }
  try {
    const handles = await window.showOpenFilePicker({
      multiple: true,
      types: [{ description: 'Audio', accept: { 'audio/*': ['.mp3','.m4a','.aac','.flac','.wav','.ogg','.oga'] } }]
    });
    const files = [];
    for (const h of handles) { files.push(await h.getFile()); }
    addFileList(files);
  } catch (e) {
    // utilisateur a annulé → rien
  }
};

function addFileList(fileList) {
  const files = Array.from(fileList || []);
  const allowedExt = /\.(mp3|m4a|aac|flac|wav|ogg|oga)$/i;
  const audios = files.filter(f => (f.type && f.type.startsWith('audio')) || allowedExt.test(f.name));
  if (!audios.length) { alert("Aucun fichier audio reconnu."); return; }
  const mapped = audios.map((f, i) => ({
    id: `${Date.now()}_${i}`,
    name: f.name.replace(/\.[^.]+$/,''),
    url: URL.createObjectURL(f),
  }));
  tracks = tracks.concat(mapped);
  renderList();
  if (tracks.length && !audio.src) setTrack(0);
}