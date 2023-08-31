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
    document.getElementById("code-editor").innerHTML = ace.edit('editor').getSession().getValue();
    document.getElementById("submit-btn").style.display = "none";
    document.getElementById("loading-btn").style.display = "inline-block";
    window.addEventListener('pageshow', function (e) {
        if (e.persisted) {
            document.getElementById("submit-btn").style.display = "inline-block";
            document.getElementById("loading-btn").style.display = "none";
        }
    });
});
