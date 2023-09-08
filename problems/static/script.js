let editor = document.getElementById('editor');

ace.edit(editor, {
    theme: 'ace/theme/xcode',
    mode: 'ace/mode/c_cpp',
    tabSize: 4,
    useSoftTabs: true,
    keyboardHandler: 'ace/keyboard/vscode',
    wrapWithQuotes: true,
});

const languages = {
    "c_cpp": "cpp",
    "java": "java",
    "python": "python"
}

document.addEventListener('submit', () => {
    document.getElementById("code-editor").innerHTML = ace.edit('editor').getSession().getValue();
    document.getElementById("get-language").innerHTML = languages[languageSelect.value]
    document.getElementById("submit-btn").style.display = "none";
    document.getElementById("loading-btn").style.display = "inline-block";
    window.addEventListener('pageshow', function (e) {
        if (e.persisted) {
            document.getElementById("submit-btn").style.display = "inline-block";
            document.getElementById("loading-btn").style.display = "none";
        }
    });
});

languageSelect.addEventListener("change", function () {
    let selectedLanguage = languageSelect.value;
    let mode = "ace/mode/" + selectedLanguage;
    ace.edit('editor').getSession().setMode(mode);
});

let onloadLanguage = languageSelect.value;
let onloadMode = "ace/mode/" + onloadLanguage;
ace.edit('editor').getSession().setMode(onloadMode);