document.addEventListener('DOMContentLoaded', function() {
    const translationsDiv = document.getElementById('translations');

    const translations = {
        wins_vs_losses: translationsDiv.getAttribute('data-wins-vs-losses'),
        points_vs_points_against: translationsDiv.getAttribute('data-points-vs-points-against'),
        ratio: translationsDiv.getAttribute('data-ratio')
    };

    const globalStatsDiv = document.getElementById('global-stats');
    const classicStatsDiv = document.getElementById('classic-stats');
    const botStatsDiv = document.getElementById('bot-stats');
    const tournamentStatsDiv = document.getElementById('tournament-stats');

    function createDoubleProgressBar(label, value1, value2, total) {
        const percentage1 = (value1 / total) * 100;
        const percentage2 = (value2 / total) * 100;
        return `
            <div class="mb-3">
                <div class="text-center">${label}</div>
                <div class="progress mb-2">
                    <div class="progress-bar bg-success" role="progressbar" style="width: ${percentage1}%" aria-valuenow="${percentage1}" aria-valuemin="0" aria-valuemax="100">${value1}</div>
                    <div class="progress-bar bg-danger" role="progressbar" style="width: ${percentage2}%" aria-valuenow="${percentage2}" aria-valuemin="0" aria-valuemax="100">${value2}</div>
                </div>
            </div>
        `;
    }

    function createProgressCircle(value) {
        const percentage = Math.min(Math.max(value, 0), 1) * 100;
        return `
            <div class="mb-3">
                <div class="progress-circle" style="width: 60px; height: 60px; position: relative; border-radius: 50%; overflow: hidden;">
                    <div style="width: 100%; height: 100%; background: conic-gradient(#4caf50 ${percentage}%, #ccc ${percentage}% 100%);"></div>
                    <span style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-weight: bold;">${value.toFixed(2)}</span>
                </div>
            </div>
        `;
    }

    // Global Stats
    globalStatsDiv.innerHTML = `
        <div class="card mb-3">
            <div class="card-body">
                ${createDoubleProgressBar(translations.wins_vs_losses, stats.global.wins, stats.global.losses, stats.global.games_played)}
                ${createDoubleProgressBar(translations.points_vs_points_against, stats.global.total_points, stats.global.total_points_against, stats.global.total_points + stats.global.total_points_against)}
                ${createProgressCircle(stats.global.ratio)}
            </div>
        </div>
    `;

    // Classic Stats
    classicStatsDiv.innerHTML = `
        <div class="card mb-3">
            <div class="card-body">
                ${createDoubleProgressBar(translations.wins_vs_losses, stats.classic.wins, stats.classic.losses, stats.classic.games_played)}
                ${createDoubleProgressBar(translations.points_vs_points_against, stats.classic.total_points, stats.classic.total_points_against, stats.classic.total_points + stats.classic.total_points_against)}
                ${createProgressCircle(stats.classic.ratio)}
            </div>
        </div>
    `;

    // Bot Stats
    botStatsDiv.innerHTML = `
        <div class="card mb-3">
            <div class="card-body">
                ${createDoubleProgressBar(translations.wins_vs_losses, stats.bot.wins, stats.bot.losses, stats.bot.games_played)}
                ${createDoubleProgressBar(translations.points_vs_points_against, stats.bot.total_points, stats.bot.total_points_against, stats.bot.total_points + stats.bot.total_points_against)}
                ${createProgressCircle(stats.bot.ratio)}
            </div>
        </div>
    `;

    // Tournament Stats
    tournamentStatsDiv.innerHTML = `
        <div class="card mb-3">
            <div class="card-body">
                ${createDoubleProgressBar(translations.wins_vs_losses, stats.tournament.wins, stats.tournament.losses, stats.tournament.games_played)}
                ${createDoubleProgressBar(translations.points_vs_points_against, stats.tournament.total_points, stats.tournament.total_points_against, stats.tournament.total_points + stats.tournament.total_points_against)}
                ${createProgressCircle(stats.tournament.ratio)}
            </div>
        </div>
    `;
});
