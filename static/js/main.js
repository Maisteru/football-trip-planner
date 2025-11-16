let leagues = [];
let teams = [];
let matches = [];

document.addEventListener('DOMContentLoaded', function() {
    loadLeagues();
    
    document.getElementById('league').addEventListener('change', function() {
        const leagueId = this.value;
        if (leagueId) {
            loadTeams(leagueId);
        }
    });
    
    document.getElementById('tripForm').addEventListener('submit', function(e) {
        e.preventDefault();
        findMatches();
    });
});

async function loadLeagues() {
    try {
        const response = await fetch('/api/leagues');
        leagues = await response.json();
        
        const leagueSelect = document.getElementById('league');
        leagues.forEach(league => {
            const option = document.createElement('option');
            option.value = league.id;
            option.textContent = `${league.name} (${league.country})`;
            leagueSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading leagues:', error);
    }
}

async function loadTeams(leagueId) {
    try {
        const response = await fetch(`/api/teams/${leagueId}`);
        teams = await response.json();
        
        const teamSelect = document.getElementById('team');
        teamSelect.innerHTML = '<option value="">Choose a team...</option>';
        teamSelect.disabled = false;
        
        teams.forEach(team => {
            const option = document.createElement('option');
            option.value = team.id;
            option.textContent = team.name;
            teamSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading teams:', error);
    }
}

async function findMatches() {
    const teamId = document.getElementById('team').value;
    const matchType = document.querySelector('input[name="matchType"]:checked').value;
    
    if (!teamId) {
        alert('Please select a team');
        return;
    }
    
    try {
        const response = await fetch('/api/matches', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                team_id: teamId,
                match_type: matchType
            })
        });
        
        matches = await response.json();
        displayMatches(matches);
    } catch (error) {
        console.error('Error finding matches:', error);
    }
}

function displayMatches(matches) {
    const matchesSection = document.getElementById('matchesSection');
    const matchesList = document.getElementById('matchesList');
    
    if (matches.length === 0) {
        matchesList.innerHTML = '<p class="text-muted">No upcoming matches found.</p>';
        matchesSection.style.display = 'block';
        return;
    }
    
    matchesList.innerHTML = '';
    matches.forEach(match => {
        const matchDate = new Date(match.date);
        const card = document.createElement('div');
        card.className = 'card mb-3';
        card.innerHTML = `
            <div class="card-body">
                <h5 class="card-title">${match.home_team} vs ${match.away_team}</h5>
                <p class="card-text">
                    <strong>Date:</strong> ${matchDate.toLocaleDateString()} ${matchDate.toLocaleTimeString()}<br>
                    <strong>Venue:</strong> ${match.venue}, ${match.city}
                </p>
                <button class="btn btn-primary" onclick="calculateTrip(${match.id})">Calculate Trip Cost</button>
            </div>
        `;
        matchesList.appendChild(card);
    });
    
    matchesSection.style.display = 'block';
}

async function calculateTrip(matchId) {
    const originCity = document.getElementById('originCity').value;
    
    if (!originCity) {
        alert('Please enter your city');
        return;
    }
    
    try {
        const response = await fetch('/api/calculate-trip', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                match_id: matchId,
                origin_city: originCity
            })
        });
        
        const data = await response.json();
        displayResults(data);
    } catch (error) {
        console.error('Error calculating trip:', error);
    }
}

function displayResults(data) {
    const matchDate = new Date(data.match.date);
    
    document.getElementById('matchInfo').innerHTML = `
        <h5>${data.match.home_team} vs ${data.match.away_team}</h5>
        <p>
            <strong>Date:</strong> ${matchDate.toLocaleDateString()} ${matchDate.toLocaleTimeString()}<br>
            <strong>Venue:</strong> ${data.match.venue}, ${data.match.city}
        </p>
    `;
    
    document.getElementById('flightCost').textContent = `€${data.costs.flight.toFixed(2)}`;
    document.getElementById('hotelCost').textContent = `€${data.costs.hotel.toFixed(2)}`;
    document.getElementById('ticketCost').textContent = `€${data.costs.ticket.toFixed(2)}`;
    document.getElementById('totalCost').textContent = `€${data.costs.total.toFixed(2)}`;
    
    if (data.links && data.links.flight) {
        const flightLink = document.getElementById('flightLink');
        flightLink.href = data.links.flight;
        flightLink.style.display = 'inline-block';
    }
    
    if (data.links && data.links.hotel) {
        const hotelLink = document.getElementById('hotelLink');
        hotelLink.href = data.links.hotel;
        hotelLink.style.display = 'inline-block';
    }
    
    document.getElementById('resultsSection').style.display = 'block';
    document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
}