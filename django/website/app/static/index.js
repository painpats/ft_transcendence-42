// Time update in the taskbar
function updateClock() {
    const now = new Date();
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    document.getElementById('clock').textContent = `${hours}:${minutes}`;
}
setInterval(updateClock, 1000);
updateClock();

document.querySelectorAll('.dropdown-item').forEach(function(item) {
    item.addEventListener('click', function() {
        const selectedLang = this.getAttribute('data-lang');
        document.documentElement.lang = selectedLang;
    });
});

// Handling the status change caca
document.querySelectorAll('.status-item').forEach(item => {
    item.addEventListener('click', function() {
        const status = this.getAttribute('data-status');
        const statusIndicator = document.getElementById('statusIndicator');
        
        if (status === 'online') {
            statusIndicator.classList.remove('status-offline');
            statusIndicator.classList.add('status-online');
            statusIndicator.setAttribute('title', 'Online');
        } else {
            statusIndicator.classList.remove('status-online');
            statusIndicator.classList.add('status-offline');
            statusIndicator.setAttribute('title', 'Offline');
        }
    });
});

// SPA CHANGE PAGE WITHOUT RELOAD
document.addEventListener('DOMContentLoaded', function () {
    document.body.addEventListener('click', function (e) {
        if (e.target.tagName === 'A' && e.target.hasAttribute('data-url')) {
            e.preventDefault();
            const url = e.target.getAttribute('data-url');
            loadPage(url);
        }
    });

    function loadPage(url) {
        fetch(url)
        .then(response => {
            if (response.status === 404) {
                window.location.href = '/404/';
                return null;
            } else {
                return response.text();
            }
        })
        .then(html => {
            if (html) {
                const tempDiv = document.createElement('div');
                tempDiv.innerHTML = html;
                const contentDiv = tempDiv.querySelector('.col-md-10');
                if (contentDiv) {
                    document.querySelector('.col-md-10').innerHTML = contentDiv.innerHTML;
                    history.pushState(null, '', url);
                }
            }
        })
        .catch(error => console.error('Erreur lors du chargement de la page:', error));
    }
    

    window.addEventListener('popstate', function () {
        loadPage(location.pathname);
    });
});


