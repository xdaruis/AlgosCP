const editor = document.getElementById('editor');

ace.edit(editor, {
    theme: 'ace/theme/eclipse',
    mode: 'ace/mode/c_cpp',
    tabSize: 4,
    useSoftTabs: true,
    keyboardHandler: 'ace/keyboard/vscode',
    wrapWithQuotes: true,
});

resize_element();

function resize_element() {
    element = document.getElementById("auto-resize");
    element.style.height = (element.scrollHeight + 2) + "px";
}

function test() {
    alert(ace.edit('editor').getSession().getValue());
}
