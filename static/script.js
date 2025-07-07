document.addEventListener('DOMContentLoaded', () => {
    const showIncidentsButton = document.getElementById('showIncidents');
    const showProblemsButton = document.getElementById('showProblems');
    const showKnowledgeButton = document.getElementById('showKnowledge');

    const incidentsSection = document.getElementById('incidentsSection');
    const problemsSection = document.getElementById('problemsSection');
    const knowledgeSection = document.getElementById('knowledgeSection');

    const createIncidentForm = document.getElementById('createIncidentForm');
    const incidentsList = document.getElementById('incidentsList');

    const createProblemForm = document.getElementById('createProblemForm');
    const problemsList = document.getElementById('problemsList');

    const createKnowledgeForm = document.getElementById('createKnowledgeForm');
    const knowledgeList = document.getElementById('knowledgeList');
    const searchKnowledgeButton = document.getElementById('searchKnowledgeButton');
    const knowledgeSearchQuery = document.getElementById('knowledgeSearchQuery');

    // Configuration commune pour tous les graphiques
    const commonChartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    boxWidth: 12,
                    padding: 15,
                    font: {
                        size: 11
                    }
                }
            }
        }
    };

    function showSection(sectionToShow) {
        incidentsSection.classList.remove('active');
        problemsSection.classList.remove('active');
        knowledgeSection.classList.remove('active');
        sectionToShow.classList.add('active');
    }

    showIncidentsButton.addEventListener('click', () => {
        showSection(incidentsSection);
        fetchIncidents();
    });

    showProblemsButton.addEventListener('click', () => {
        showSection(problemsSection);
        fetchProblems();
    });

    showKnowledgeButton.addEventListener('click', () => {
        showSection(knowledgeSection);
        fetchKnowledgeArticles();
    });

    // Initial display
    showSection(incidentsSection);
    fetchIncidents();

    // Incident Management
    createIncidentForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const title = document.getElementById('incidentTitle').value;
        const description = document.getElementById('incidentDescription').value;
        const priority = document.getElementById('incidentPriority').value;

        try {
            const response = await fetch('/incidents/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ title, description, priority }),
            });
            if (response.ok) {
                createIncidentForm.reset();
                fetchIncidents();
            } else {
                console.error('Failed to create incident');
                alert('Erreur lors de la création de l\'incident.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Une erreur est survenue lors de la communication avec le serveur.');
        }
    });

    async function fetchIncidents() {
        try {
            const response = await fetch('/incidents/');
            if (response.ok) {
                const incidents = await response.json();
                incidentsList.innerHTML = '';
                incidents.forEach(incident => {
                    const incidentCard = document.createElement('div');
                    incidentCard.classList.add('item-card');
                    incidentCard.innerHTML = `
                        <h4>${incident.title} (ID: ${incident.id})</h4>
                        <p><strong>Description:</strong> ${incident.description}</p>
                        <p><strong>Priorité:</strong> ${incident.priority}</p>
                        <p><strong>Statut:</strong> ${incident.status}</p>
                        <p><strong>Créé le:</strong> ${new Date(incident.created_at).toLocaleString()}</p>
                        <p><strong>Mis à jour le:</strong> ${new Date(incident.updated_at).toLocaleString()}</p>
                    `;
                    incidentsList.appendChild(incidentCard);
                });
            } else {
                console.error('Failed to fetch incidents');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }

    // Problem Management
    createProblemForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const title = document.getElementById('problemTitle').value;
        const description = document.getElementById('problemDescription').value;
        const root_cause = document.getElementById('problemRootCause').value;

        try {
            const response = await fetch('/problems/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ title, description, root_cause }),
            });
            if (response.ok) {
                createProblemForm.reset();
                fetchProblems();
            } else {
                console.error('Failed to create problem');
                alert('Erreur lors de la création du problème.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Une erreur est survenue lors de la communication avec le serveur.');
        }
    });

    async function fetchProblems() {
        try {
            const response = await fetch('/problems/');
            if (response.ok) {
                const problems = await response.json();
                problemsList.innerHTML = '';
                problems.forEach(problem => {
                    const problemCard = document.createElement('div');
                    problemCard.classList.add('item-card');
                    problemCard.innerHTML = `
                        <h4>${problem.title} (ID: ${problem.id})</h4>
                        <p><strong>Description:</strong> ${problem.description}</p>
                        <p><strong>Cause Racine:</strong> ${problem.root_cause}</p>
                        <p><strong>Statut:</strong> ${problem.status}</p>
                        <p><strong>Créé le:</strong> ${new Date(problem.created_at).toLocaleString()}</p>
                        <p><strong>Mis à jour le:</strong> ${new Date(problem.updated_at).toLocaleString()}</p>
                    `;
                    problemsList.appendChild(problemCard);
                });
            } else {
                console.error('Failed to fetch problems');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }

    // Knowledge Base Management
    createKnowledgeForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const title = document.getElementById('knowledgeTitle').value;
        const content = document.getElementById('knowledgeContent').value;
        const tags = document.getElementById('knowledgeTags').value;

        try {
            const response = await fetch('/knowledge/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ title, content, tags, author_id: 1 }), // Assuming author_id 1 for now
            });
            if (response.ok) {
                createKnowledgeForm.reset();
                fetchKnowledgeArticles();
            } else {
                console.error('Failed to create knowledge article');
                alert('Erreur lors de la création de l\'article de connaissance.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Une erreur est survenue lors de la communication avec le serveur.');
        }
    });

    searchKnowledgeButton.addEventListener('click', () => {
        const query = knowledgeSearchQuery.value;
        if (query) {
            fetchKnowledgeArticles(query);
        } else {
            fetchKnowledgeArticles();
        }
    });

    async function fetchKnowledgeArticles(query = '') {
        try {
            const url = query ? `/knowledge/search/?query=${encodeURIComponent(query)}` : '/knowledge/';
            const response = await fetch(url);
            if (response.ok) {
                const articles = await response.json();
                knowledgeList.innerHTML = '';
                articles.forEach(article => {
                    const articleCard = document.createElement('div');
                    articleCard.classList.add('item-card');
                    articleCard.innerHTML = `
                        <h4>${article.title} (ID: ${article.id})</h4>
                        <p><strong>Contenu:</strong> ${article.content}</p>
                        <p><strong>Tags:</strong> ${article.tags}</p>
                        <p><strong>Créé le:</strong> ${new Date(article.created_at).toLocaleString()}</p>
                        <p><strong>Mis à jour le:</strong> ${new Date(article.updated_at).toLocaleString()}</p>
                    `;
                    knowledgeList.appendChild(articleCard);
                });
            } else {
                console.error('Failed to fetch knowledge articles');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }

    // Fonction pour créer un graphique en camembert
    function createPieChart(ctx, data, labels) {
        return new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: [
                        '#4e73df',
                        '#1cc88a',
                        '#36b9cc',
                        '#f6c23e'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                ...commonChartOptions,
                cutout: '60%'
            }
        });
    }

    // Fonction pour créer un graphique linéaire
    function createLineChart(ctx, labels, data, label) {
        return new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: label,
                    data: data,
                    borderColor: '#4e73df',
                    backgroundColor: 'rgba(78, 115, 223, 0.05)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.3
                }]
            },
            options: {
                ...commonChartOptions,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    }
                }
            }
        });
    }

    // Mise à jour des graphiques avec les données du serveur
    function updateDashboardCharts() {
        fetch('/api/dashboard_stats')
            .then(response => response.json())
            .then(data => {
                // Graphique des incidents par statut
                const incidentStatusCtx = document.getElementById('incidentStatusChart');
                if (incidentStatusCtx) {
                    const incidentLabels = Object.keys(data.incident_status);
                    const incidentData = Object.values(data.incident_status);
                    createPieChart(incidentStatusCtx, incidentData, incidentLabels);
                }

                // Graphique des problèmes par statut
                const problemStatusCtx = document.getElementById('problemStatusChart');
                if (problemStatusCtx) {
                    const problemLabels = Object.keys(data.problem_status);
                    const problemData = Object.values(data.problem_status);
                    createPieChart(problemStatusCtx, problemData, problemLabels);
                }

                // Graphique d'évolution des incidents
                const incidentEvolutionCtx = document.getElementById('incidentEvolutionChart');
                if (incidentEvolutionCtx) {
                    const incidentEvolutionLabels = data.incident_evolution.map(item => item.date);
                    const incidentEvolutionData = data.incident_evolution.map(item => item.count);
                    createLineChart(incidentEvolutionCtx, incidentEvolutionLabels, incidentEvolutionData, 'Incidents');
                }

                // Graphique d'évolution des problèmes
                const problemEvolutionCtx = document.getElementById('problemEvolutionChart');
                if (problemEvolutionCtx) {
                    const problemEvolutionLabels = data.problem_evolution.map(item => item.date);
                    const problemEvolutionData = data.problem_evolution.map(item => item.count);
                    createLineChart(problemEvolutionCtx, problemEvolutionLabels, problemEvolutionData, 'Problèmes');
                }
            })
            .catch(error => {
                console.error('Erreur lors de la récupération des données:', error);
            });
    }

    // Initialiser les graphiques au chargement de la page
    if (document.getElementById('incidentStatusChart')) {
        updateDashboardCharts();
    }
}); 