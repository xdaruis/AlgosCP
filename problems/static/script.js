let editor = document.getElementById('editor');

ace.edit(editor, {
    theme: 'ace/theme/xcode',
    mode: 'ace/mode/c_cpp',
    tabSize: 4,
    useSoftTabs: true,
    keyboardHandler: 'ace/keyboard/vscode',
    wrapWithQuotes: true,
});

document.addEventListener('submit', () => {
    document.getElementById("submit-btn").style.display = "none";
    document.getElementById("loading-btn").style.display = "inline-block";
    document.getElementById("code-editor").innerHTML = ace.edit('editor').getSession().getValue();
});