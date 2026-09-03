// Student Workspace & Dashboard View (Section 41 & 12 Navigation Fixes)
const DashboardView = {
  async render() {
    const user = API.getCurrentUser();
    if (!user) {
      window.location.hash = '#/login';
      return;
    }

    const container = document.getElementById('app-view');
    if (!container) return;

    container.innerHTML = `
      <section class="section-padding" style="background-color: var(--color-gray-bg);">
        <div class="container">
          <!-- Back Navigation Bar (Section 12 Fix) -->
          <div style="margin-bottom: 20px;">
            <a href="#/" class="btn btn-outline btn-sm" style="display: inline-flex; align-items: center; gap: 6px;">
              <i data-feather="arrow-left" style="width:14px; height:14px;"></i> ← Back to Home
            </a>
          </div>

          <!-- Header Bar -->
          <div style="background: var(--color-white); border-radius: var(--radius-lg); padding: 32px; border: 1px solid var(--color-border); margin-bottom: 32px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 20px;">
            <div>
              <span class="badge-sector" style="margin-bottom: 8px; display: inline-block;">STUDENT WORKSPACE</span>
              <h1 style="font-size: 32px; color: var(--color-blue-dark); margin: 0;">Welcome back, ${user.full_name || user.name || 'Student'}! 👋</h1>
              <p style="color: var(--color-gray-text); font-size: 14px; margin-top: 4px;">Track active virtual internship applications, submit weekly PDF deliverables, and access official documents.</p>
            </div>
            <div style="display:flex; gap:12px;">
              <button onclick="DashboardView.switchTab('applications')" id="tab-btn-apps" class="btn btn-primary">My Internships</button>
              <button onclick="DashboardView.switchTab('documents')" id="tab-btn-docs" class="btn btn-outline">My Documents</button>
              <a href="#/internships" class="btn btn-outline">+ Explore Internships</a>
            </div>
          </div>

          <!-- Applications View Tab -->
          <div id="tab-content-apps">
            <div id="dashboard-apps-list">
              <div style="text-align: center; padding: 40px; background: white; border-radius: var(--radius-lg);">Loading your workspace...</div>
            </div>
          </div>

          <!-- My Documents View Tab (Section 41 Requirement) -->
          <div id="tab-content-docs" style="display: none;">
            <div id="dashboard-docs-list">
              <div style="text-align: center; padding: 40px; background: white; border-radius: var(--radius-lg);">Loading official documents...</div>
            </div>
          </div>
        </div>
      </section>
    `;

    if (window.feather) feather.replace();
    await this.loadApplications();
    await this.loadDocuments();
  },

  switchTab(tabName) {
    const appsContent = document.getElementById('tab-content-apps');
    const docsContent = document.getElementById('tab-content-docs');
    const btnApps = document.getElementById('tab-btn-apps');
    const btnDocs = document.getElementById('tab-btn-docs');

    if (tabName === 'documents') {
      appsContent.style.display = 'none';
      docsContent.style.display = 'block';
      btnApps.className = 'btn btn-outline';
      btnDocs.className = 'btn btn-primary';
    } else {
      appsContent.style.display = 'block';
      docsContent.style.display = 'none';
      btnApps.className = 'btn btn-primary';
      btnDocs.className = 'btn btn-outline';
    }
  },

  async loadApplications() {
    try {
      const res = await API.request('/api/applications/me');
      const container = document.getElementById('dashboard-apps-list');
      if (!container) return;

      if (!res.applications || res.applications.length === 0) {
        container.innerHTML = `
          <div style="background: white; border-radius: var(--radius-lg); padding: 48px; text-align: center; border: 1px solid var(--color-border);">
            <i data-feather="book-open" style="width: 48px; height: 48px; color: var(--color-accent-blue); margin-bottom: 16px;"></i>
            <h3 style="font-size: 22px; color: var(--color-blue-dark); margin-bottom: 8px;">No Active Internships Found</h3>
            <p style="color: var(--color-gray-text); margin-bottom: 24px;">You haven't enrolled in any virtual internship program yet.</p>
            <a href="#/internships" class="btn btn-primary">Browse Available Internships →</a>
          </div>
        `;
        if (window.feather) feather.replace();
        return;
      }

      container.innerHTML = res.applications.map(app => `
        <div style="background: var(--color-white); border-radius: var(--radius-lg); border: 1px solid var(--color-border); padding: 32px; margin-bottom: 24px; box-shadow: var(--shadow-sm);">
          <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; flex-wrap: wrap; gap: 12px;">
            <div>
              <span class="badge-sector">${app.sector_name}</span>
              <h2 style="font-size: 24px; color: var(--color-blue-dark); margin-top: 6px;">${app.internship_title}</h2>
              <p style="font-size: 13px; color: var(--color-gray-text); margin-top: 2px;">
                Start Date: <strong>${app.start_date || 'N/A'}</strong> | Target End Date: <strong>${app.end_date || 'N/A'}</strong>
              </p>
            </div>
            <div style="display: flex; gap: 12px; flex-wrap: wrap;">
              <a href="/api/applications/${app.id}/offer-letter.pdf" target="_blank" class="btn btn-outline btn-sm">
                <i data-feather="file-text" style="width:14px;"></i> View Offer Letter PDF
              </a>
              ${app.certificate_id ? `
                <a href="/api/certificates/${app.certificate_id}/pdf" target="_blank" class="btn btn-primary btn-sm">
                  <i data-feather="award" style="width:14px;"></i> Certificate PDF
                </a>
              ` : `
                <span class="btn btn-outline btn-sm" style="opacity: 0.7; cursor: not-allowed;" title="Available upon completion after end date">
                  🔒 Certificate (Not Available Yet)
                </span>
              `}
            </div>
          </div>

          <!-- Progress Bar -->
          <div style="margin-bottom: 24px;">
            <div style="display: flex; justify-content: space-between; font-size: 14px; font-weight: 600; margin-bottom: 8px;">
              <span style="color: var(--color-blue-dark);">Module Progress: Week ${app.completed_weeks} of ${app.duration_weeks} Completed</span>
              <span style="color: var(--color-accent-blue);">${app.progress_percent}%</span>
            </div>
            <div class="progress-bar-track">
              <div class="progress-bar-fill" style="width: ${app.progress_percent}%;"></div>
            </div>
          </div>

          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 13px; color: var(--color-gray-text);">
              Status: <strong style="color: #0B3D91; text-transform: uppercase;">${app.status || 'ACTIVE'}</strong>
            </span>
            <button onclick="DashboardView.openWorkspace('${app.id}')" class="btn btn-primary">
              Open Task Workspace & Submit Assignments →
            </button>
          </div>
        </div>
      `).join('');

      if (window.feather) feather.replace();
    } catch (e) {
      console.error("Load applications error:", e);
    }
  },

  async loadDocuments() {
    try {
      const res = await API.request('/api/applications/me');
      const container = document.getElementById('dashboard-docs-list');
      if (!container) return;

      if (!res.applications || res.applications.length === 0) {
        container.innerHTML = `<div style="background: white; border-radius: var(--radius-lg); padding: 40px; text-align: center;">No document records found.</div>`;
        return;
      }

      container.innerHTML = `
        <div style="background: var(--color-white); border-radius: var(--radius-lg); border: 1px solid var(--color-border); padding: 32px;">
          <h2 style="font-size: 22px; color: var(--color-blue-dark); margin-bottom: 20px;">My Official Documents</h2>
          
          <div style="display: flex; flex-direction: column; gap: 20px;">
            ${res.applications.map(app => `
              <!-- Offer Letter Box -->
              <div style="border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 20px; background: #F8FAFC;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
                  <div>
                    <h3 style="font-size: 18px; color: var(--color-blue-dark); margin: 0;">Internship Offer Letter</h3>
                    <p style="font-size: 14px; color: var(--color-gray-text); margin-top: 4px;">Program: <strong>${app.internship_title}</strong></p>
                    <span style="font-size: 12px; font-weight: 700; color: #10B981; background: #D1FAE5; padding: 4px 10px; border-radius: 99px;">STATUS: ISSUED</span>
                  </div>
                  <div style="display: flex; gap: 10px;">
                    <a href="/api/applications/${app.id}/offer-letter.pdf" target="_blank" class="btn btn-outline btn-sm">
                      [View]
                    </a>
                    <a href="/api/applications/${app.id}/offer-letter.pdf" download class="btn btn-primary btn-sm">
                      [Download]
                    </a>
                  </div>
                </div>
              </div>

              <!-- Certificate Box -->
              <div style="border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 20px; background: #F8FAFC;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
                  <div>
                    <h3 style="font-size: 18px; color: var(--color-blue-dark); margin: 0;">Internship Completion Certificate</h3>
                    <p style="font-size: 14px; color: var(--color-gray-text); margin-top: 4px;">Program: <strong>${app.internship_title}</strong></p>
                    ${app.certificate_id ? `
                      <span style="font-size: 12px; font-weight: 700; color: #0B3D91; background: #EAF1FB; padding: 4px 10px; border-radius: 99px;">
                        STATUS: ISSUED (ID: ${app.certificate_id})
                      </span>
                    ` : `
                      <span style="font-size: 12px; font-weight: 700; color: #D97706; background: #FEF3C7; padding: 4px 10px; border-radius: 99px;">
                        STATUS: NOT AVAILABLE YET (Issued on/after ${app.end_date || 'completion date'})
                      </span>
                    `}
                  </div>
                  <div style="display: flex; gap: 10px;">
                    ${app.certificate_id ? `
                      <a href="/api/certificates/${app.certificate_id}/pdf" target="_blank" class="btn btn-outline btn-sm">
                        [View]
                      </a>
                      <a href="/api/certificates/${app.certificate_id}/pdf" download class="btn btn-primary btn-sm">
                        [Download]
                      </a>
                    ` : `
                      <button class="btn btn-outline btn-sm" disabled style="opacity: 0.5;">[Not Available Yet]</button>
                    `}
                  </div>
                </div>
              </div>
            `).join('')}
          </div>
        </div>
      `;
    } catch (e) {
      console.error("Load documents error:", e);
    }
  },

  async openWorkspace(appId) {
    try {
      const res = await API.request(`/api/applications/${appId}`);
      const app = res.application;

      let html = `
        <div style="max-width: 650px;">
          <!-- Back button in modal (Section 12 Navigation Fix) -->
          <div style="margin-bottom: 16px;">
            <button onclick="Modals.close()" class="btn btn-outline btn-sm">
              ← Back to Assignments List
            </button>
          </div>

          <h2 style="font-size: 22px; color: var(--color-blue-dark); margin-bottom: 8px;">Task Workspace: ${app.internship_title}</h2>
          <p style="color: var(--color-gray-text); font-size: 14px; margin-bottom: 20px;">Upload PDF deliverables (Max 10MB) for weekly evaluations.</p>

          <div style="display: flex; flex-direction: column; gap: 16px; margin-bottom: 24px;">
            ${app.tasks.map(t => {
              const sub = t.submission;
              const subStatus = sub ? sub.status : 'NOT_SUBMITTED';
              let badgeColor = '#9CA3AF';
              if (['graded', 'approved'].includes(subStatus.toLowerCase())) badgeColor = '#10B981';
              if (subStatus.toLowerCase() === 'submitted' || subStatus.toLowerCase() === 'pending') badgeColor = '#3B82F6';
              if (['revise', 'rejected', 'late'].includes(subStatus.toLowerCase())) badgeColor = '#EF4444';

              return `
                <div style="border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 18px; background: var(--color-gray-bg);">
                  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <strong style="color: var(--color-blue-dark); font-size: 15px;">Week ${t.week_number}: ${t.title}</strong>
                    <span style="font-size: 11px; font-weight: 700; color: white; background: ${badgeColor}; padding: 3px 10px; border-radius: 99px; text-transform: uppercase;">
                      ${subStatus.replace('_', ' ')}
                    </span>
                  </div>
                  <p style="font-size: 13px; color: var(--color-gray-text); margin-bottom: 8px;"><strong>Deliverables:</strong> ${t.deliverables}</p>

                  <!-- Marks & Feedback Display (Section 24 Requirement) -->
                  ${sub && sub.marks !== null && sub.marks !== undefined ? `
                    <div style="font-size: 13px; background: #ECFDF5; border-left: 4px solid #10B981; padding: 10px; margin: 10px 0; color: #065F46; border-radius: 4px;">
                      <strong>Marks Obtained:</strong> ${sub.marks} / ${sub.max_marks || 10} <br/>
                      <strong>Admin Feedback:</strong> ${sub.feedback || 'Great work! Assignment approved.'}
                    </div>
                  ` : ''}

                  <form onsubmit="DashboardView.submitPdfFile(event, '${app.id}', ${t.week_number})" style="margin-top: 12px;">
                    <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                      <input type="file" id="pdf-file-${t.week_number}" accept=".pdf,application/pdf" class="form-input" style="font-size: 12px; padding: 6px;" />
                      <button type="submit" class="btn btn-primary btn-sm" style="white-space: nowrap;">
                        ${sub ? 'Re-upload PDF' : 'Upload & Submit PDF'}
                      </button>
                    </div>
                    <span style="font-size: 11px; color: #64748B;">Accepted format: PDF files only (Max size 10MB).</span>
                  </form>
                </div>
              `;
            }).join('')}
          </div>
        </div>
      `;

      Modals.open(html);
    } catch (e) {
      Toast.show(e.message || 'Failed to open workspace.', 'error');
    }
  },

  async submitPdfFile(event, appId, weekNumber) {
    event.preventDefault();
    const fileInput = document.getElementById(`pdf-file-${weekNumber}`);
    if (!fileInput.files || fileInput.files.length === 0) {
      Toast.show('Please select a PDF file to upload.', 'error');
      return;
    }

    const file = fileInput.files[0];
    if (!file.name.toLowerCase().endsWith('.pdf')) {
      Toast.show('Only PDF files (.pdf) are allowed.', 'error');
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      Toast.show('File size exceeds 10MB limit.', 'error');
      return;
    }

    const formData = new FormData();
    formData.append('application_id', appId);
    formData.append('week_number', weekNumber);
    formData.append('file', file);

    try {
      Toast.show(`Uploading Week ${weekNumber} assignment PDF...`, 'info');
      const token = localStorage.getItem('access_token');
      const res = await fetch('/api/submissions/upload', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
        body: formData
      });
      const data = await res.json();
      if (res.ok) {
        Toast.show(data.message || 'Assignment PDF uploaded successfully!', 'success');
        Modals.close();
        this.loadApplications();
      } else {
        Toast.show(data.error || 'PDF upload failed.', 'error');
      }
    } catch (e) {
      Toast.show(e.message || 'Task upload failed.', 'error');
    }
  }
};
