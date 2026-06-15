// main.js — students will add JavaScript here as features are built

(function () {
    var root = document.documentElement;
    var btn = document.getElementById('themeToggle');

    var stored = localStorage.getItem('theme');
    var prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    var isDark = stored ? stored === 'dark' : prefersDark;

    if (isDark) {
        root.setAttribute('data-theme', 'dark');
        btn.textContent = '☀';
    }

    btn.addEventListener('click', function () {
        var dark = root.getAttribute('data-theme') === 'dark';
        if (dark) {
            root.removeAttribute('data-theme');
            localStorage.setItem('theme', 'light');
            btn.textContent = '☾';
        } else {
            root.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
            btn.textContent = '☀';
        }
    });
})();
