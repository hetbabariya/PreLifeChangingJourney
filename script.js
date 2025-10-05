// Test data and state management
let currentTestIndex = -1; // Start at -1 for welcome screen
let testResults = {};
let navigationHistory = ['welcomeScreen'];

const tests = [
    'mbtiScreen',
    'intelligenceScreen', 
    'bigFiveScreen',
    'riasecScreen',
    'decisionScreen',
    'lifeScreen',
    'varkScreen'
];

const testNames = {
    'mbtiScreen': 'MBTI Personality',
    'intelligenceScreen': 'Multiple Intelligence',
    'bigFiveScreen': 'Big Five Personality',
    'riasecScreen': 'RIASEC Career Interest',
    'decisionScreen': 'Decision Making Style',
    'lifeScreen': 'Life Situation',
    'varkScreen': 'VARK Learning Style'
};

const testSteps = {
    'welcomeScreen': 'Welcome',
    'mbtiScreen': 'MBTI Test',
    'intelligenceScreen': 'Intelligence Test',
    'bigFiveScreen': 'Big Five Test',
    'riasecScreen': 'RIASEC Test',
    'decisionScreen': 'Decision Test',
    'lifeScreen': 'Life Assessment',
    'varkScreen': 'Learning Style',
    'resultsScreen': 'Results'
};

// Test descriptions will be loaded from test-data.js

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
    updateProgressBar();
    updateBackButton();
    updateProgressText('welcomeScreen');
});

function setupEventListeners() {
    // Add click listeners to all option cards
    document.querySelectorAll('.option-card').forEach(card => {
        card.addEventListener('click', function() {
            selectOption(this);
        });
    });
}

function startTests() {
    showScreen('mbtiScreen');
    currentTestIndex = 0;
    navigationHistory.push('mbtiScreen');
    updateProgressBar();
    updateBackButton();
}

function showScreen(screenId) {
    // Hide all screens
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    
    // Show target screen with animation
    const targetScreen = document.getElementById(screenId);
    targetScreen.classList.add('active', 'fade-in');
    
    // Remove animation class after animation completes
    setTimeout(() => {
        targetScreen.classList.remove('fade-in');
    }, 500);
    
    // Update progress text
    updateProgressText(screenId);
}

function selectOption(selectedCard) {
    const currentScreen = document.querySelector('.screen.active');
    const allCards = currentScreen.querySelectorAll('.option-card');
    
    // Remove selection from all cards in current test
    allCards.forEach(card => {
        card.classList.remove('selected');
    });
    
    // Add selection to clicked card
    selectedCard.classList.add('selected');
    
    // Store the result
    const testId = currentScreen.id;
    const value = selectedCard.getAttribute('data-value');
    testResults[testId] = value;
    
    // Enable next button
    const nextButton = currentScreen.querySelector('.btn-next');
    if (nextButton) {
        nextButton.disabled = false;
    }
    
    // Add selection animation
    selectedCard.style.transform = 'scale(1.05)';
    setTimeout(() => {
        selectedCard.style.transform = '';
    }, 200);
}

function nextTest() {
    currentTestIndex++;
    
    if (currentTestIndex < tests.length) {
        const nextScreen = tests[currentTestIndex];
        navigationHistory.push(nextScreen);
        showScreen(nextScreen);
        updateProgressBar();
        updateBackButton();
    }
}

function updateProgressBar() {
    const progress = ((currentTestIndex + 1) / (tests.length + 1)) * 100;
    const progressFill = document.getElementById('progressFill');
    const progressCount = document.getElementById('progressCount');
    
    progressFill.style.width = progress + '%';
    
    if (currentTestIndex === -1) {
        progressCount.textContent = '0/7';
    } else if (currentTestIndex >= tests.length) {
        progressCount.textContent = '7/7';
    } else {
        progressCount.textContent = `${currentTestIndex + 1}/7`;
    }
}

function updateProgressText(screenId) {
    const progressText = document.getElementById('progressText');
    progressText.textContent = testSteps[screenId] || 'Assessment';
}

function updateBackButton() {
    const backButton = document.getElementById('backButton');
    
    if (navigationHistory.length > 1) {
        backButton.style.display = 'flex';
    } else {
        backButton.style.display = 'none';
    }
}

function goBack() {
    if (navigationHistory.length > 1) {
        // Remove current screen from history
        navigationHistory.pop();
        
        // Get previous screen
        const previousScreen = navigationHistory[navigationHistory.length - 1];
        
        // Update current test index
        if (previousScreen === 'welcomeScreen') {
            currentTestIndex = -1;
        } else {
            currentTestIndex = tests.indexOf(previousScreen);
        }
        
        // Show previous screen
        showScreen(previousScreen);
        updateProgressBar();
        updateBackButton();
        
        // Clear selection if going back to a test
        if (tests.includes(previousScreen)) {
            const testScreen = document.getElementById(previousScreen);
            const selectedCard = testScreen.querySelector('.option-card.selected');
            if (selectedCard) {
                selectedCard.classList.remove('selected');
                delete testResults[previousScreen];
                
                // Disable next button
                const nextButton = testScreen.querySelector('.btn-next');
                if (nextButton) {
                    nextButton.disabled = true;
                }
            }
        }
    }
}

async function generateReport() {
    // Show loading state
    const button = document.querySelector('#varkScreen .btn-next');
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating AI Insights...';
    button.disabled = true;
    
    try {
        // Generate AI insights
        const aiInsights = await generateAIInsights();
        
        // Store insights for display
        window.aiInsights = aiInsights;
        
        // Navigate to results
        navigationHistory.push('resultsScreen');
        showScreen('resultsScreen');
        displayResults();
        currentTestIndex = tests.length; // Set to completed state
        updateProgressBar();
        updateBackButton();
        
        showNotification('AI insights generated successfully!', 'success');
        
    } catch (error) {
        console.error('Error generating AI insights:', error);
        showNotification('AI insights generation failed. Please try again or check your internet connection.', 'error');
        
        // Show basic results without AI insights
        navigationHistory.push('resultsScreen');
        showScreen('resultsScreen');
        displayResults();
        currentTestIndex = tests.length;
        updateProgressBar();
        updateBackButton();
        
        // Add retry button to results page
        setTimeout(() => {
            const resultsActions = document.querySelector('.results-actions');
            if (resultsActions && !resultsActions.querySelector('.retry-ai-btn')) {
                const retryBtn = document.createElement('button');
                retryBtn.className = 'btn-secondary retry-ai-btn';
                retryBtn.innerHTML = '<i class="fas fa-redo"></i> Retry AI Insights';
                retryBtn.onclick = async () => {
                    retryBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
                    retryBtn.disabled = true;
                    try {
                        const aiInsights = await generateAIInsights();
                        window.aiInsights = aiInsights;
                        displayResults();
                        showNotification('AI insights generated successfully!', 'success');
                        retryBtn.remove();
                    } catch (error) {
                        showNotification('AI insights generation failed again. Please check your connection.', 'error');
                        retryBtn.innerHTML = '<i class="fas fa-redo"></i> Retry AI Insights';
                        retryBtn.disabled = false;
                    }
                };
                resultsActions.appendChild(retryBtn);
            }
        }, 100);
    } finally {
        // Reset button
        button.innerHTML = originalText;
        button.disabled = false;
    }
}

async function generateAIInsights(retryCount = 0) {
    const maxRetries = 2;
    
    try {
        const response = await fetch('/api/generate-insights', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                testResults: testResults
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            return data.insights;
        } else {
            // If the server suggests retry and we haven't exceeded max retries
            if (data.retry_suggested && retryCount < maxRetries) {
                console.log(`Retrying AI insights generation (attempt ${retryCount + 2}/${maxRetries + 1})...`);
                await new Promise(resolve => setTimeout(resolve, 2000)); // Wait 2 seconds before retry
                return await generateAIInsights(retryCount + 1);
            } else {
                throw new Error(data.error || 'Failed to generate AI insights');
            }
        }
        
    } catch (error) {
        console.error('API Error:', error);
        
        // If it's a network error and we haven't exceeded max retries
        if (retryCount < maxRetries && (error.message.includes('fetch') || error.message.includes('network'))) {
            console.log(`Retrying due to network error (attempt ${retryCount + 2}/${maxRetries + 1})...`);
            await new Promise(resolve => setTimeout(resolve, 2000));
            return await generateAIInsights(retryCount + 1);
        }
        
        // If all retries failed, throw the error (no fallback)
        throw error;
    }
}


function displayAIInsights(container) {
    const insights = window.aiInsights;
    
    // AI Insights Header
    const aiHeader = document.createElement('div');
    aiHeader.className = 'ai-insights-header';
    aiHeader.innerHTML = `
        <h2><i class="fas fa-robot"></i> AI-Powered Career Insights | AI આધારિત કારકિર્દી માર્ગદર્શન</h2>
        <p>તમારા મનોવૈજ્ઞાનિક મૂલ્યાંકનના આધારે વ્યક્તિગત ભલામણો</p>
    `;
    container.appendChild(aiHeader);
    
    // Best Field Recommendation with enhanced display
    const bestFieldCard = document.createElement('div');
    bestFieldCard.className = 'result-card ai-insight-card best-field-card';
    bestFieldCard.innerHTML = `
        <h3><i class="fas fa-bullseye"></i> શ્રેષ્ઠ કારકિર્દી ક્ષેત્ર | Best Career Field</h3>
        <div class="ai-field-name">${insights.best_field.field}</div>
        <div class="match-percentage">
            <span class="percentage-label">મેચ પર્સેન્ટેજ:</span>
            <span class="percentage-value">${insights.best_field.match_percentage || 85}%</span>
        </div>
        <div class="ai-reasoning">${insights.best_field.reasoning}</div>
        
        <div class="field-details">
            <div class="detail-item">
                <strong>ગુજરાતમાં તકો:</strong>
                <p>${insights.best_field.gujarat_opportunities}</p>
            </div>
            <div class="detail-item">
                <strong>પગાર અપેક્ષા:</strong>
                <p>${insights.best_field.salary_expectations}</p>
            </div>
            <div class="detail-item">
                <strong>કંપનીઓ:</strong>
                <div class="company-tags">
                    ${insights.best_field.specific_companies?.map(company => `<span class="company-tag">${company}</span>`).join('') || ''}
                </div>
            </div>
        </div>
    `;
    container.appendChild(bestFieldCard);
    
    // Enhanced Career Recommendations
    const careerCard = document.createElement('div');
    careerCard.className = 'result-card ai-insight-card';
    careerCard.innerHTML = `
        <h3><i class="fas fa-briefcase"></i> કારકિર્દી ભલામણો | Career Recommendations</h3>
        <div class="career-list">
            ${insights.career_recommendations.map(career => `
                <div class="career-item enhanced-career">
                    <div class="career-header">
                        <strong class="job-role">${career.job_role}</strong>
                        <span class="industry-tag">${career.industry}</span>
                    </div>
                    <p class="career-explanation">${career.explanation}</p>
                    <div class="career-details">
                        <div class="detail-row">
                            <span class="label">વૃદ્ધિ સંભાવના:</span>
                            <span class="value growth-${career.growth_potential?.toLowerCase()}">${career.growth_potential}</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">પગાર શ્રેણી:</span>
                            <span class="value salary">${career.salary_range}</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">જરૂરી કુશળતા:</span>
                            <div class="skills-tags">
                                ${career.required_skills?.map(skill => `<span class="skill-tag">${skill}</span>`).join('') || ''}
                            </div>
                        </div>
                    </div>
                </div>
            `).join('')}
        </div>
    `;
    container.appendChild(careerCard);
    
    // Enhanced Skills & Roadmap
    const skillsCard = document.createElement('div');
    skillsCard.className = 'result-card ai-insight-card';
    skillsCard.innerHTML = `
        <h3><i class="fas fa-cogs"></i> કુશળતા અને શિક્ષણ માર્ગ | Skills & Learning Roadmap</h3>
        <div class="skills-section">
            <div class="skills-grid">
                <div class="technical-skills">
                    <h4><i class="fas fa-code"></i> તકનીકી કુશળતા:</h4>
                    <div class="skills-list">
                        ${insights.skill_recommendations.technical_skills.map(skillObj => `
                            <div class="skill-item">
                                <span class="skill-name">${typeof skillObj === 'object' ? skillObj.skill : skillObj}</span>
                                ${typeof skillObj === 'object' ? `<span class="importance ${skillObj.importance?.toLowerCase()}">${skillObj.importance}</span>` : ''}
                            </div>
                        `).join('')}
                    </div>
                </div>
                
                <div class="soft-skills">
                    <h4><i class="fas fa-users"></i> સોફ્ટ સ્કિલ્સ:</h4>
                    <div class="skills-list">
                        ${insights.skill_recommendations.soft_skills.map(skillObj => `
                            <div class="skill-item">
                                <span class="skill-name">${typeof skillObj === 'object' ? skillObj.skill : skillObj}</span>
                                ${typeof skillObj === 'object' ? `<span class="importance ${skillObj.importance?.toLowerCase()}">${skillObj.importance}</span>` : ''}
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
            
            <h4><i class="fas fa-map-marked-alt"></i> શિક્ષણ માર્ગ:</h4>
            <div class="roadmap enhanced-roadmap">
                <div class="roadmap-item short-term">
                    <div class="roadmap-header">
                        <strong>${insights.roadmap.short_term.duration}</strong>
                        <span class="phase-label">તાત્કાલિક</span>
                    </div>
                    <div class="roadmap-content">
                        <div class="goals">
                            <strong>લક્ષ્યો:</strong>
                            <ul>${insights.roadmap.short_term.goals?.map(goal => `<li>${goal}</li>`).join('') || ''}</ul>
                        </div>
                        <div class="actions">
                            <strong>કાર્યો:</strong>
                            <ul>${insights.roadmap.short_term.specific_actions?.map(action => `<li>${action}</li>`).join('') || ''}</ul>
                        </div>
                    </div>
                </div>
                
                <div class="roadmap-item mid-term">
                    <div class="roadmap-header">
                        <strong>${insights.roadmap.mid_term.duration}</strong>
                        <span class="phase-label">મધ્યમ ગાળો</span>
                    </div>
                    <div class="roadmap-content">
                        <div class="goals">
                            <strong>લક્ષ્યો:</strong>
                            <ul>${insights.roadmap.mid_term.goals?.map(goal => `<li>${goal}</li>`).join('') || ''}</ul>
                        </div>
                        <div class="milestones">
                            <strong>પડાવો:</strong>
                            <ul>${insights.roadmap.mid_term.milestones?.map(milestone => `<li>${milestone}</li>`).join('') || ''}</ul>
                        </div>
                    </div>
                </div>
                
                <div class="roadmap-item long-term">
                    <div class="roadmap-header">
                        <strong>${insights.roadmap.long_term.duration}</strong>
                        <span class="phase-label">લાંબા ગાળો</span>
                    </div>
                    <div class="roadmap-content">
                        <div class="goals">
                            <strong>લક્ષ્યો:</strong>
                            <ul>${insights.roadmap.long_term.goals?.map(goal => `<li>${goal}</li>`).join('') || ''}</ul>
                        </div>
                        <div class="entrepreneurship">
                            <strong>ઉદ્યોગસાહસિક તકો:</strong>
                            <p>${insights.roadmap.long_term.entrepreneurship_opportunities || ''}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    container.appendChild(skillsCard);
    
    // Enhanced Strengths & Weaknesses Analysis
    const analysisCard = document.createElement('div');
    analysisCard.className = 'result-card ai-insight-card';
    analysisCard.innerHTML = `
        <h3><i class="fas fa-chart-line"></i> શક્તિઓ અને સુધારાના ક્ષેત્રો | Strengths & Areas for Improvement</h3>
        <div class="analysis-section enhanced-analysis">
            <div class="strengths">
                <h4><i class="fas fa-plus-circle"></i> તમારી શક્તિઓ:</h4>
                <div class="strength-items">
                    ${insights.result_analysis.strengths.map(strengthObj => `
                        <div class="strength-item">
                            <strong class="strength-title">${typeof strengthObj === 'object' ? strengthObj.strength : strengthObj}</strong>
                            ${typeof strengthObj === 'object' ? `
                                <p class="strength-reasoning">${strengthObj.reasoning}</p>
                                <p class="career-application"><strong>કારકિર્દીમાં ઉપયોગ:</strong> ${strengthObj.career_application}</p>
                            ` : ''}
                        </div>
                    `).join('')}
                </div>
            </div>
            
            <div class="weaknesses">
                <h4><i class="fas fa-exclamation-triangle"></i> સુધારાના ક્ષેત્રો:</h4>
                <div class="weakness-items">
                    ${insights.result_analysis.weaknesses.map(weaknessObj => `
                        <div class="weakness-item">
                            <strong class="weakness-title">${typeof weaknessObj === 'object' ? weaknessObj.weakness : weaknessObj}</strong>
                            ${typeof weaknessObj === 'object' ? `
                                <p class="weakness-reasoning">${weaknessObj.reasoning}</p>
                                <p class="improvement-strategy"><strong>સુધારાની રીત:</strong> ${weaknessObj.improvement_strategy}</p>
                            ` : ''}
                        </div>
                    `).join('')}
                </div>
            </div>
        </div>
    `;
    container.appendChild(analysisCard);
    
    // Enhanced Future Plans
    const futureCard = document.createElement('div');
    futureCard.className = 'result-card ai-insight-card';
    futureCard.innerHTML = `
        <h3><i class="fas fa-rocket"></i> ભવિષ્યની વૃદ્ધિ યોજના | Future Growth Plans</h3>
        <div class="future-plans enhanced-future">
            <div class="plan-item three-year">
                <div class="plan-header">
                    <strong>3 વર્ષની યોજના</strong>
                    <span class="timeline-badge">2027</span>
                </div>
                <div class="plan-content">
                    <p class="position"><strong>અપેક્ષિત પદ:</strong> ${insights.future_plans['3_year_plan']?.career_position || insights.future_plans['3_year_plan']}</p>
                    ${insights.future_plans['3_year_plan']?.key_achievements ? `
                        <div class="achievements">
                            <strong>મુખ્ય સિદ્ધિઓ:</strong>
                            <ul>${insights.future_plans['3_year_plan'].key_achievements.map(achievement => `<li>${achievement}</li>`).join('')}</ul>
                        </div>
                    ` : ''}
                </div>
            </div>
            
            <div class="plan-item five-year">
                <div class="plan-header">
                    <strong>5 વર્ષની યોજના</strong>
                    <span class="timeline-badge">2029</span>
                </div>
                <div class="plan-content">
                    <p class="position"><strong>વરિષ્ઠ પદ:</strong> ${insights.future_plans['5_year_plan']?.career_position || insights.future_plans['5_year_plan']}</p>
                    ${insights.future_plans['5_year_plan']?.expertise_areas ? `
                        <div class="expertise">
                            <strong>નિપુણતા ક્ષેત્રો:</strong>
                            <div class="expertise-tags">
                                ${insights.future_plans['5_year_plan'].expertise_areas.map(area => `<span class="expertise-tag">${area}</span>`).join('')}
                            </div>
                        </div>
                    ` : ''}
                </div>
            </div>
            
            <div class="plan-item ten-year">
                <div class="plan-header">
                    <strong>10 વર્ષની દ્રષ્ટિ</strong>
                    <span class="timeline-badge">2034</span>
                </div>
                <div class="plan-content">
                    <p class="vision"><strong>કારકિર્દી દ્રષ્ટિ:</strong> ${insights.future_plans['10_year_plan']?.career_vision || insights.future_plans['10_year_plan']}</p>
                    ${insights.future_plans['10_year_plan']?.entrepreneurial_potential ? `
                        <p class="entrepreneurship"><strong>ઉદ્યોગસાહસિક સંભાવના:</strong> ${insights.future_plans['10_year_plan'].entrepreneurial_potential}</p>
                    ` : ''}
                </div>
            </div>
        </div>
    `;
    container.appendChild(futureCard);
    
    // Enhanced Daily Habits
    const habitsCard = document.createElement('div');
    habitsCard.className = 'result-card ai-insight-card';
    habitsCard.innerHTML = `
        <h3><i class="fas fa-calendar-check"></i> દૈનિક સફળતાની આદતો | Daily Success Habits</h3>
        <div class="habits-list enhanced-habits">
            ${insights.daily_habits.map(habitObj => `
                <div class="habit-item">
                    <div class="habit-header">
                        <strong class="habit-name">${typeof habitObj === 'object' ? habitObj.habit : habitObj}</strong>
                    </div>
                    ${typeof habitObj === 'object' ? `
                        <p class="habit-purpose"><strong>હેતુ:</strong> ${habitObj.purpose}</p>
                        <p class="habit-implementation"><strong>અમલીકરણ:</strong> ${habitObj.implementation}</p>
                    ` : ''}
                </div>
            `).join('')}
        </div>
    `;
    container.appendChild(habitsCard);
    
    // Enhanced Certifications
    const certsCard = document.createElement('div');
    certsCard.className = 'result-card ai-insight-card';
    certsCard.innerHTML = `
        <h3><i class="fas fa-certificate"></i> ભલામણ કરેલ પ્રમાણપત્રો | Recommended Certifications</h3>
        <div class="certifications-list enhanced-certs">
            ${insights.certifications.map(cert => `
                <div class="cert-item enhanced-cert">
                    <div class="cert-header">
                        <h4 class="cert-name">${cert.name}</h4>
                        <div class="cert-badges">
                            <span class="provider-badge">${cert.provider}</span>
                            <span class="level-badge ${cert.difficulty_level?.toLowerCase()}">${cert.difficulty_level}</span>
                        </div>
                    </div>
                    <p class="cert-recommendation">${cert.why_recommended}</p>
                    <div class="cert-details">
                        <span class="duration"><i class="fas fa-clock"></i> ${cert.estimated_duration}</span>
                    </div>
                    <a href="${cert.direct_enrollment_link}" target="_blank" class="btn-primary cert-link">
                        <i class="fas fa-external-link-alt"></i> હવે નોંધણી કરો | Enroll Now
                    </a>
                </div>
            `).join('')}
        </div>
    `;
    container.appendChild(certsCard);
    
    // Additional Insights
    if (insights.additional_insights) {
        const additionalCard = document.createElement('div');
        additionalCard.className = 'result-card ai-insight-card';
        additionalCard.innerHTML = `
            <h3><i class="fas fa-lightbulb"></i> વધારાની સૂઝ | Additional Insights</h3>
            <div class="additional-insights">
                <div class="insight-item">
                    <strong>કામનું વાતાવરણ:</strong>
                    <p>${insights.additional_insights.work_environment}</p>
                </div>
                <div class="insight-item">
                    <strong>તણાવ સંચાલન:</strong>
                    <p>${insights.additional_insights.stress_management}</p>
                </div>
                <div class="insight-item gujarat-specific">
                    <strong>ગુજરાત વિશેષ સલાહ:</strong>
                    <p>${insights.additional_insights.gujarat_specific_advice}</p>
                </div>
            </div>
        `;
        container.appendChild(additionalCard);
    }
}

function displayResults() {
    const resultsContent = document.getElementById('resultsContent');
    resultsContent.innerHTML = '';
    
    // Display AI Insights if available
    if (window.aiInsights) {
        displayAIInsights(resultsContent);
    }
    
    // Create a modern results overview section
    if (!window.aiInsights) {
        const overviewCard = document.createElement('div');
        overviewCard.className = 'result-card summary-card';
        overviewCard.innerHTML = `
            <h3><i class="fas fa-chart-line"></i> Assessment Overview</h3>
            <div class="result-description">
                <strong>Your Psychological Profile Summary</strong><br><br>
                You've completed ${Object.keys(testResults).length} comprehensive psychological assessments. 
                Below are your detailed results with personalized insights and recommendations.
            </div>
        `;
        resultsContent.appendChild(overviewCard);
    }

    // Create result cards for each test with clean, modern design
    Object.keys(testResults).forEach(testId => {
        const testName = testNames[testId];
        const result = testResults[testId];
        let detailedInfo = getDetailedTestInfo(testId, result);
        
        const resultCard = document.createElement('div');
        resultCard.className = 'result-card detailed-result';
        resultCard.innerHTML = `
            <h3><i class="fas fa-check-circle"></i> ${testName}</h3>
            <div class="result-value">${result}</div>
            <div class="result-title">${detailedInfo.title}</div>
            ${detailedInfo.gujarati ? `<div class="result-gujarati">${detailedInfo.gujarati}</div>` : ''}
            <div class="result-description">${detailedInfo.description}</div>
            
            ${detailedInfo.strengths ? `<div class="result-strengths"><strong>Key Strengths:</strong> ${detailedInfo.strengths}</div>` : ''}
            ${detailedInfo.challenges ? `<div class="result-challenges"><strong>Growth Areas:</strong> ${detailedInfo.challenges}</div>` : ''}
            ${detailedInfo.careers ? `<div class="result-careers"><strong>Career Paths:</strong> ${detailedInfo.careers}</div>` : ''}
            ${detailedInfo.traits ? `<div class="result-traits"><strong>Key Traits:</strong> ${Array.isArray(detailedInfo.traits) ? detailedInfo.traits.join(', ') : detailedInfo.traits}</div>` : ''}
            ${detailedInfo.work_environment ? `<div class="result-environment"><strong>Ideal Environment:</strong> ${detailedInfo.work_environment}</div>` : ''}
            ${detailedInfo.learning_methods ? `<div class="result-methods"><strong>Learning Style:</strong> ${Array.isArray(detailedInfo.learning_methods) ? detailedInfo.learning_methods.join(', ') : detailedInfo.learning_methods}</div>` : ''}
            ${detailedInfo.study_tips ? `<div class="result-tips"><strong>Study Tips:</strong> ${Array.isArray(detailedInfo.study_tips) ? detailedInfo.study_tips.join(', ') : detailedInfo.study_tips}</div>` : ''}
        `;
        
        resultsContent.appendChild(resultCard);
    });
    
    // Add comprehensive summary card
    const summaryCard = document.createElement('div');
    summaryCard.className = 'result-card summary-card';
    summaryCard.style.gridColumn = '1 / -1';
    summaryCard.innerHTML = `
        <h3><i class="fas fa-star"></i> Comprehensive Assessment Summary</h3>
        <div class="result-description">
            <strong>Your Complete Psychological Profile:</strong><br><br>
            Based on your responses across ${Object.keys(testResults).length} different psychological assessments, 
            you demonstrate a unique combination of personality traits, cognitive abilities, learning preferences, 
            and decision-making styles. This comprehensive profile provides deep insights into your psychological makeup.<br><br>
            
            <strong>Profile Overview:</strong><br>
            ${generateProfileSummary()}<br><br>
            
            <strong>Key Recommendations:</strong><br>
            • Leverage your ${testResults.mbtiScreen || 'personality type'} strengths in professional settings<br>
            • Develop your ${testResults.intelligenceScreen || 'dominant intelligence'} through targeted activities<br>
            • Use ${testResults.varkScreen || 'your learning style'} methods for optimal learning<br>
            • Consider ${testResults.riasecScreen || 'career-aligned'} professional opportunities<br>
            • Apply your ${testResults.decisionScreen || 'decision-making style'} awareness in important choices<br><br>
            
            <strong>Personal Development Areas:</strong><br>
            This assessment reveals both your natural strengths and areas for potential growth. 
            Use these insights for career planning, relationship building, learning optimization, 
            and personal development strategies.
        </div>
    `;
    
    resultsContent.appendChild(summaryCard);
}

function getDetailedTestInfo(testId, result) {
    // Map test screen IDs to data categories
    const testMapping = {
        'mbtiScreen': 'mbti',
        'intelligenceScreen': 'intelligence', 
        'bigFiveScreen': 'bigFive',
        'riasecScreen': 'riasec',
        'decisionScreen': 'decisionMaking',
        'lifeScreen': 'lifeSituation',
        'varkScreen': 'vark'
    };
    
    const category = testMapping[testId];
    if (category && testData[category] && testData[category][result]) {
        return testData[category][result];
    }
    
    return {
        title: result.toUpperCase(),
        description: 'Detailed information not available for this result.'
    };
}

function generateProfileSummary() {
    let summary = '';
    
    if (testResults.mbtiScreen) {
        const mbtiInfo = testData.mbti[testResults.mbtiScreen];
        summary += `• <strong>Personality:</strong> ${mbtiInfo?.title || testResults.mbtiScreen} - ${mbtiInfo?.description || 'Your core personality type'}<br>`;
    }
    
    if (testResults.intelligenceScreen) {
        const intInfo = testData.intelligence[testResults.intelligenceScreen];
        summary += `• <strong>Intelligence:</strong> ${intInfo?.title || testResults.intelligenceScreen} - ${intInfo?.description || 'Your dominant intelligence type'}<br>`;
    }
    
    if (testResults.bigFiveScreen) {
        const bigFiveInfo = testData.bigFive[testResults.bigFiveScreen];
        summary += `• <strong>Personality Trait:</strong> ${bigFiveInfo?.title || testResults.bigFiveScreen} - ${bigFiveInfo?.description || 'Your dominant personality dimension'}<br>`;
    }
    
    if (testResults.riasecScreen) {
        const riasecInfo = testData.riasec[testResults.riasecScreen];
        summary += `• <strong>Career Interest:</strong> ${riasecInfo?.title || testResults.riasecScreen} - ${riasecInfo?.description || 'Your career preference area'}<br>`;
    }
    
    if (testResults.decisionScreen) {
        const decisionInfo = testData.decisionMaking[testResults.decisionScreen];
        summary += `• <strong>Decision Style:</strong> ${decisionInfo?.title || testResults.decisionScreen} - ${decisionInfo?.description || 'Your decision-making approach'}<br>`;
    }
    
    if (testResults.lifeScreen) {
        const lifeInfo = testData.lifeSituation[testResults.lifeScreen];
        summary += `• <strong>Life Focus:</strong> ${lifeInfo?.title || testResults.lifeScreen} - ${lifeInfo?.description || 'Your current life priority'}<br>`;
    }
    
    if (testResults.varkScreen) {
        const varkInfo = testData.vark[testResults.varkScreen];
        summary += `• <strong>Learning Style:</strong> ${varkInfo?.title || testResults.varkScreen} - ${varkInfo?.description || 'Your preferred learning method'}<br>`;
    }
    
    return summary;
}

async function downloadReport() {
    try {
        // Show loading state
        const downloadBtn = document.querySelector('.results-actions .btn-primary');
        const originalText = downloadBtn.innerHTML;
        downloadBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating PDF...';
        downloadBtn.disabled = true;
        
        // Prepare data for PDF generation
        const reportData = {
            testResults: testResults,
            aiInsights: window.aiInsights || null
        };
        
        // First try to generate markdown content
        try {
            const markdownResponse = await fetch('/api/generate-markdown', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(reportData)
            });
            
            if (markdownResponse.ok) {
                const markdownData = await markdownResponse.json();
                if (markdownData.success) {
                    // Convert markdown to PDF using client-side approach
                    convertMarkdownToPDF(markdownData.markdown);
                    showNotification('PDF preview opened! Use Print/Save as PDF to download.', 'success');
                    return;
                }
            }
        } catch (markdownError) {
            console.log('Markdown generation failed, falling back to server PDF:', markdownError);
        }
        
        // Fallback to server-side PDF generation
        const response = await fetch('/api/download-report', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(reportData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        // Get the PDF blob
        const blob = await response.blob();
        
        // Create download link
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        
        // Generate filename with timestamp
        const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-');
        a.download = `Psychological_Report_${timestamp}.pdf`;
        
        // Trigger download
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        
        // Show success message
        showNotification('PDF report downloaded successfully!', 'success');
        
        // Reset button
        downloadBtn.innerHTML = originalText;
        downloadBtn.disabled = false;
        
    } catch (error) {
        console.error('Error downloading report:', error);
        
        // Show error message with retry option
        showNotification('AI insights generation failed. Please try again or check your internet connection.', 'error');
        
        // Show basic results without AI insights
        navigationHistory.push('resultsScreen');
        showScreen('resultsScreen');
        displayResults();
        currentTestIndex = tests.length;
        updateProgressBar();
        updateBackButton();
        
        // Add retry button
        const retryBtn = document.createElement('button');
        retryBtn.className = 'btn btn-primary';
        retryBtn.innerHTML = '<i class="fas fa-redo"></i> Retry AI Insights Generation';
        retryBtn.onclick = () => {
            generateAIInsights();
        };
        const resultsActions = document.querySelector('.results-actions');
        resultsActions.appendChild(retryBtn);
        
        // Reset button
        const downloadBtn = document.querySelector('.results-actions .btn-primary');
        if (downloadBtn) {
            downloadBtn.innerHTML = '<i class="fas fa-download"></i> Download Report';
        }
    }
}

function downloadTextReport() {
    // Fallback text report generation
    let reportContent = `
COMPREHENSIVE PSYCHOLOGICAL ASSESSMENT REPORT
Generated on: ${new Date().toLocaleDateString()}
Time: ${new Date().toLocaleTimeString()}

===========================================
DETAILED ASSESSMENT RESULTS:
===========================================

`;

    Object.keys(testResults).forEach(testId => {
        const testName = testNames[testId];
        const result = testResults[testId];
        const detailedInfo = getDetailedTestInfo(testId, result);
        
        reportContent += `
${testName.toUpperCase()}:
Result: ${result.toUpperCase()}
Title: ${detailedInfo.title}
Description: ${detailedInfo.description}
${detailedInfo.strengths ? `Strengths: ${detailedInfo.strengths}` : ''}
${detailedInfo.challenges ? `Challenges: ${detailedInfo.challenges}` : ''}
${detailedInfo.careers ? `Career Suggestions: ${detailedInfo.careers}` : ''}

-------------------------------------------
`;
    });

    // Add AI insights if available
    if (window.aiInsights) {
        reportContent += `

===========================================
AI-POWERED INSIGHTS:
===========================================

RECOMMENDED CAREER FIELD: ${window.aiInsights.best_field?.field || 'Not available'}
REASONING: ${window.aiInsights.best_field?.reasoning || 'Not available'}

CAREER RECOMMENDATIONS:
${window.aiInsights.career_recommendations?.map(career => `- ${career.role}: ${career.explanation}`).join('\n') || 'Not available'}

SKILLS TO DEVELOP:
Technical: ${window.aiInsights.skill_recommendations?.technical_skills?.join(', ') || 'Not available'}
Soft Skills: ${window.aiInsights.skill_recommendations?.soft_skills?.join(', ') || 'Not available'}

DAILY HABITS:
${window.aiInsights.daily_habits?.map(habit => `- ${habit}`).join('\n') || 'Not available'}
`;
    }

    reportContent += `

===========================================
DISCLAIMER:
===========================================

This report is generated based on your responses to psychological assessments and is intended for educational and self-reflection purposes only.

Report generated by: AI-Powered Psychological Testing Platform
Generation Date: ${new Date().toLocaleString()}
`;

    // Create and download the text file
    const blob = new Blob([reportContent], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = `Psychological_Assessment_Report_${new Date().toISOString().slice(0, 10)}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

function restartTests() {
    // Reset all data
    currentTestIndex = -1;
    testResults = {};
    navigationHistory = ['welcomeScreen'];
    
    // Clear all selections
    document.querySelectorAll('.option-card').forEach(card => {
        card.classList.remove('selected');
    });
    
    // Disable all next buttons
    document.querySelectorAll('.btn-next').forEach(button => {
        button.disabled = true;
    });
    
    // Show welcome screen
    showScreen('welcomeScreen');
    updateProgressBar();
    updateBackButton();
    
    showNotification('Assessment reset. Ready to start again!', 'info');
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check' : 'info'}-circle"></i>
        ${message}
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#4CAF50' : '#2196F3'};
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        z-index: 1000;
        display: flex;
        align-items: center;
        gap: 10px;
        font-weight: 500;
        animation: slideInRight 0.3s ease-out;
    `;
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease-in forwards';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Add keyboard navigation
document.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
        const activeScreen = document.querySelector('.screen.active');
        const nextButton = activeScreen.querySelector('.btn-next:not(:disabled)');
        if (nextButton) {
            nextButton.click();
        }
    }
});

// Add smooth scrolling for better UX
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('option-card')) {
        e.target.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'center' 
        });
    }
});

// Performance optimization: Lazy load animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('slide-in-right');
        }
    });
}, observerOptions);

// Observe all option cards for animation
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.option-card').forEach(card => {
        observer.observe(card);
    });
});

// Markdown to PDF conversion functions
function convertMarkdownToPDF(markdownContent) {
    try {
        // Create a temporary HTML content from markdown
        const htmlContent = convertMarkdownToHTML(markdownContent);
        
        // Create a new window for PDF generation
        const printWindow = window.open('', '_blank');
        printWindow.document.write(`
            <!DOCTYPE html>
            <html>
            <head>
                <title>Psychological Assessment Report</title>
                <style>
                    body {
                        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                        line-height: 1.6;
                        color: #2d3748;
                        max-width: 800px;
                        margin: 0 auto;
                        padding: 40px 20px;
                        background: white;
                    }
                    h1 {
                        color: #667eea;
                        font-size: 28px;
                        font-weight: 800;
                        text-align: center;
                        margin-bottom: 30px;
                        border-bottom: 3px solid #667eea;
                        padding-bottom: 15px;
                    }
                    h2 {
                        color: #667eea;
                        font-size: 20px;
                        font-weight: 700;
                        margin-top: 40px;
                        margin-bottom: 20px;
                        border-left: 4px solid #667eea;
                        padding-left: 15px;
                    }
                    h3 {
                        color: #4c51bf;
                        font-size: 16px;
                        font-weight: 600;
                        margin-top: 25px;
                        margin-bottom: 15px;
                    }
                    h4 {
                        color: #2d3748;
                        font-size: 14px;
                        font-weight: 600;
                        margin-top: 20px;
                        margin-bottom: 10px;
                    }
                    p {
                        margin-bottom: 12px;
                        font-size: 12px;
                        line-height: 1.6;
                    }
                    .field-name {
                        font-size: 18px;
                        font-weight: 800;
                        color: #2d3748;
                        text-align: center;
                        background: #f7fafc;
                        padding: 15px;
                        border-radius: 8px;
                        border: 2px solid #e2e8f0;
                        margin: 20px 0;
                    }
                    .match-percentage {
                        font-size: 24px;
                        font-weight: 800;
                        color: #f6ad55;
                        text-align: center;
                        background: #fffaf0;
                        padding: 15px;
                        border-radius: 8px;
                        border: 2px solid #fed7aa;
                        margin: 15px 0;
                    }
                    .highlight {
                        background: #edf2f7;
                        padding: 12px;
                        border-radius: 6px;
                        border-left: 4px solid #667eea;
                        margin: 10px 0;
                    }
                    .info-box {
                        background: #f0f4f8;
                        border: 1px solid #cbd5e0;
                        border-radius: 8px;
                        padding: 15px;
                        margin: 15px 0;
                    }
                    .career-item {
                        background: #f7fafc;
                        border: 1px solid #e2e8f0;
                        border-radius: 8px;
                        padding: 15px;
                        margin: 15px 0;
                    }
                    .roadmap-section {
                        background: #f8f9fa;
                        border: 1px solid #dee2e6;
                        border-radius: 8px;
                        padding: 15px;
                        margin: 15px 0;
                    }
                    .strength-item {
                        background: #f0fff4;
                        border-left: 4px solid #48bb78;
                        padding: 12px;
                        margin: 10px 0;
                        border-radius: 0 6px 6px 0;
                    }
                    .weakness-item {
                        background: #fffaf0;
                        border-left: 4px solid #ed8936;
                        padding: 12px;
                        margin: 10px 0;
                        border-radius: 0 6px 6px 0;
                    }
                    .cert-item {
                        background: #f0f4f8;
                        border: 1px solid #cbd5e0;
                        border-radius: 8px;
                        padding: 15px;
                        margin: 15px 0;
                    }
                    .footer {
                        margin-top: 50px;
                        padding-top: 20px;
                        border-top: 2px solid #e2e8f0;
                        font-size: 10px;
                        color: #718096;
                        text-align: center;
                    }
                    ul {
                        margin-left: 20px;
                        margin-bottom: 15px;
                    }
                    li {
                        margin-bottom: 8px;
                        font-size: 12px;
                    }
                    strong {
                        font-weight: 600;
                        color: #2d3748;
                    }
                    em {
                        font-style: italic;
                        color: #4a5568;
                    }
                    @media print {
                        body { margin: 0; padding: 20px; font-size: 11px; }
                        .no-print { display: none; }
                        h1 { font-size: 24px; }
                        h2 { font-size: 18px; }
                        h3 { font-size: 14px; }
                        .field-name { font-size: 16px; }
                        .match-percentage { font-size: 20px; }
                    }
                </style>
            </head>
            <body>
                ${htmlContent}
                <div class="no-print" style="text-align: center; margin-top: 30px; padding: 20px; background: #f7fafc; border-radius: 8px;">
                    <h3 style="margin-bottom: 15px; color: #667eea;">Ready to Save as PDF?</h3>
                    <p style="margin-bottom: 20px; color: #4a5568;">Use your browser's print function to save this report as a PDF file.</p>
                    <button onclick="window.print()" style="background: #667eea; color: white; border: none; padding: 12px 24px; border-radius: 6px; cursor: pointer; font-size: 14px; margin-right: 10px;">
                        🖨️ Print/Save as PDF
                    </button>
                    <button onclick="window.close()" style="background: #e2e8f0; color: #2d3748; border: none; padding: 12px 24px; border-radius: 6px; cursor: pointer; font-size: 14px;">
                        ✖️ Close
                    </button>
                </div>
            </body>
            </html>
        `);
        printWindow.document.close();
        
        // Focus the new window
        printWindow.focus();
        
    } catch (error) {
        console.error('Error converting markdown to PDF:', error);
        showNotification('Failed to convert to PDF. Please try the fallback download.', 'error');
    }
}

// Enhanced markdown to HTML converter
function convertMarkdownToHTML(markdown) {
    let html = markdown;
    
    // Convert headers
    html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');
    html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
    html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
    html = html.replace(/^#### (.*$)/gim, '<h4>$1</h4>');
    
    // Convert bold and italic
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
    
    // Convert horizontal rules
    html = html.replace(/^---$/gim, '<hr>');
    
    // Convert lists (improved handling)
    html = html.replace(/^- (.*$)/gim, '<li>$1</li>');
    html = html.replace(/^\* (.*$)/gim, '<li>$1</li>');
    
    // Wrap consecutive li elements in ul
    html = html.replace(/(<li>.*?<\/li>\s*)+/gs, function(match) {
        return '<ul>' + match + '</ul>';
    });
    
    // Convert line breaks to paragraphs (improved)
    const lines = html.split('\n');
    let result = '';
    let inParagraph = false;
    let inList = false;
    
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        
        if (line === '') {
            if (inParagraph) {
                result += '</p>\n';
                inParagraph = false;
            }
            if (inList) {
                inList = false;
            }
        } else if (line.startsWith('<h') || line.startsWith('<hr') || line.startsWith('<ul') || line.startsWith('</ul>')) {
            if (inParagraph) {
                result += '</p>\n';
                inParagraph = false;
            }
            result += line + '\n';
            if (line.startsWith('<ul')) {
                inList = true;
            } else if (line.startsWith('</ul>')) {
                inList = false;
            }
        } else if (line.startsWith('<li>')) {
            if (inParagraph) {
                result += '</p>\n';
                inParagraph = false;
            }
            result += line + '\n';
        } else {
            if (!inParagraph && !inList) {
                result += '<p>';
                inParagraph = true;
            } else if (inParagraph) {
                result += ' ';
            }
            result += line;
        }
    }
    
    if (inParagraph) {
        result += '</p>\n';
    }
    
    // Clean up formatting
    result = result.replace(/<p><\/p>/g, '');
    result = result.replace(/<p>\s*<\/p>/g, '');
    result = result.replace(/\n\s*\n/g, '\n');
    
    // Add special styling for field names and percentages
    result = result.replace(/<p><strong>([^<]*)<\/strong><\/p>/g, '<div class="field-name">$1</div>');
    result = result.replace(/<p><strong>Match Percentage: (\d+)%<\/strong><\/p>/g, '<div class="match-percentage">Match Percentage: $1%</div>');
    
    return result;
}
