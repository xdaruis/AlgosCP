let editor = document.getElementById('editor');

ace.edit(editor, {
    theme: 'ace/theme/xcode',
    mode: 'ace/mode/c_cpp',
    tabSize: 4,
    useSoftTabs: true,
    keyboardHandler: 'ace/keyboard/vscode',
    wrapWithQuotes: true,
});

function test() {
    alert(ace.edit('editor').getSession().getValue());
}

document.addEventListener('submit', () => {
    document.getElementById("code-editor").innerHTML = ace.edit('editor').getSession().getValue();
});