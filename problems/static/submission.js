let editor = document.getElementById("editor");

ace.edit(editor, {
  theme: "ace/theme/xcode",
  mode: "ace/mode/c_cpp",
  tabSize: 4,
  useSoftTabs: true,
  keyboardHandler: "ace/keyboard/vscode",
  wrapWithQuotes: true,
  setUseWorker: false,
  readOnly: true,
});
