let editor = document.getElementById('editor');

let prefferedLanguage = localStorage.getItem('selectedLanguage');
if (prefferedLanguage) {
  languageSelect.value = prefferedLanguage;
  prefferedLanguage = 'ace/mode/' + prefferedLanguage;
} else {
  prefferedLanguage = 'ace/mode/c_cpp';
}

ace.edit(editor, {
  theme: 'ace/theme/xcode',
  mode: prefferedLanguage,
  tabSize: 4,
  useSoftTabs: true,
  keyboardHandler: 'ace/keyboard/vscode',
});

const aceEditor = ace.edit('editor').getSession();

const languages = {
  c_cpp: 'cpp',
  java: 'java',
  python: 'python',
};

var socket = new WebSocket('ws://' + window.location.host + '/ws/solution/');

socket.onopen = function (e) {
  console.log('[open] Connection established');
};

socket.onmessage = function (event) {
  console.log(`[message] Data received from server: ${event.data}`);
};

socket.onclose = function (event) {
  if (event.wasClean) {
    console.log(
      `[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`,
    );
  } else {
    console.log('[close] Connection died');
  }
};

document.addEventListener('submit', () => {
  document.getElementById('code-editor').innerHTML = aceEditor.getValue();
  document.getElementById('get-language').innerHTML =
    languages[languageSelect.value];
  document.getElementById('submit-btn').style.display = 'none';
  document.getElementById('loading-btn').style.display = 'inline-block';
  socket.send('Form submitted');
  window.addEventListener('pageshow', function (e) {
    if (e.persisted) {
      document.getElementById('submit-btn').style.display = 'inline-block';
      document.getElementById('loading-btn').style.display = 'none';
    }
  });
});

languageSelect.addEventListener('change', function () {
  let selectedLanguage = languageSelect.value;
  let mode = 'ace/mode/' + selectedLanguage;
  aceEditor.setMode(mode);
  localStorage.setItem('selectedLanguage', selectedLanguage);
});

aceEditor.on('change', () => {
  localStorage.setItem('editorContent' + actId, aceEditor.getValue());
  localStorage.setItem('editorContent' + actId, aceEditor.getValue());
});

let onloadLanguage = languageSelect.value;
let onloadMode = 'ace/mode/' + onloadLanguage;
aceEditor.setMode(onloadMode);

const actId = document.getElementById('problem-id').value;
const savedContent = localStorage.getItem('editorContent' + actId);
if (savedContent) {
  aceEditor.setValue(savedContent);
}

function resetTemplate() {
  aceEditor.setValue(document.getElementById('default-template').value);
  languageSelect.value = 'c_cpp';
  localStorage.setItem('selectedLanguage', 'c_cpp');
  aceEditor.setMode('ace/mode/c_cpp');
}
