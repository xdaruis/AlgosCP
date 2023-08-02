let editor = document.getElementById('editor');

ace.edit(editor, {
    theme: 'ace/theme/chrome',
    mode: 'ace/mode/c_cpp',
    tabSize: 4,
    useSoftTabs: true,
    keyboardHandler: 'ace/keyboard/vscode',
    wrapWithQuotes: true,
});

resize_boxes();

function resize_boxes() {
    for (let i = 1; i <= 3; ++i) {
        element = document.getElementById("note" + i);
        element.style.height = (element.scrollHeight + 2) + "px";
    }
}