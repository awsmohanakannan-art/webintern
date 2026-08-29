// Student Workspace & Dashboard View
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
          <!-- Header Bar -->
          <div style="background: var(--color-white); border-radius: var(--radius-lg); padding: 32px; border: 1px solid var(--color-border); margin-bottom: 32px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 20px;">
            <div>
              <span class="badge-sector" style="margin-bottom: 8px; display: inline-block;">STUDENT WORKSPACE</span>
              <h1 style="font-size: 32px; color: var(--color-blue-dark); margin: 0;">Welcome back, ${user.name || 'Student'}! 👋</h1>
              <p style="color: var(--color-gray-text); font-size: 14px; margin-top: 4px;">Track active virtual internship applications, submit weekly deliverables, and claim certificates.</p>
            </div>
            <a href="#/internships" class="btn btn-primary">+ Explore New Internship</a>
          </div>

          <!-- Applications Workspace List -->
          <div id="dashboard-apps-list">
            <div style="text-align: center; padding: 40px; background: white; border-radius: var(--radius-lg);">Loading your applications...</div>
          </div>
        </div>
      </section>
    `;

    await this.loadApplications();
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
            </div>
            <div style="display: flex; gap: 12px;">
              <a href="/api/applications/${app.id}/offer-letter.pdf" target="_blank" class="btn btn-outline btn-sm">
                <i data-feather="file-text" style="width:14px;"></i> Offer Letter PDF
              </a>
              ${app.certificate_id ? `
                <a href="/api/certificates/${app.certificate_id}/pdf" target="_blank" class="btn btn-primary btn-sm">
                  <i data-feather="award" style="width:14px;"></i> Certificate PDF
                </a>
                ${!app.is_verified_paid ? `
                  <button onclick="Modals.openRazorpayCheckout('${app.certificate_id}')" class="btn btn-outline btn-sm" style="border-color: #F59E0B; color: #D97706;">
                    ⚡ Upgrade Certificate (₹499)
                  </button>
                ` : `<span class="badge-mode" style="background:#D1FAE5; color:#065F46;">✅ Verified Paid</span>`}
              ` : ''}
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

          <div style="text-align: right;">
            <button onclick="DashboardView.openWorkspace('${app.id}')" class="btn btn-primary">
              Open Task Workspace & Deliverables →
            </button>
          </div>
        </div>
      `).join('');

      if (window.feather) feather.replace();
    } catch (e) {
      console.error("Load applications error:", e);
    }
  },

  async openWorkspace(appId) {
    try {
      const res = await API.request(`/api/applications/${appId}`);
      const app = res.application;

      let html = `
        <div style="max-width: 600px;">
          <h2 style="font-size: 22px; color: var(--color-blue-dark); margin-bottom: 12px;">Task Workspace: ${app.internship_title}</h2>
          <p style="color: var(--color-gray-text); font-size: 14px; margin-bottom: 20px;">Submit weekly deliverables for admin review.</p>

          <div style="display: flex; flex-direction: column; gap: 16px; margin-bottom: 24px;">
            ${app.tasks.map(t => {
              const sub = t.submission;
              const subStatus = sub ? sub.status : 'not_submitted';
              let badgeColor = '#9CA3AF';
              if (subStatus === 'approved') badgeColor = '#10B981';
              if (subStatus === 'pending') badgeColor = '#3B82F6';
              if (subStatus === 'revise') badgeColor = '#EF4444';

              return `
                <div style="border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 16px; background: var(--color-gray-bg);">
                  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <strong style="color: var(--color-blue-dark);">Week ${t.week_number}: ${t.title}</strong>
                    <span style="font-size: 11px; font-weight: 700; color: white; background: ${badgeColor}; padding: 3px 10px; border-radius: 99px; text-transform: uppercase;">
                      ${subStatus.replace('_', ' ')}
                    </span>
                  </div>
                  <p style="font-size: 13px; color: var(--color-gray-text); margin-bottom: 12px;"><strong>Deliverable:</strong> ${t.deliverables}</p>

                  ${sub && sub.feedback ? `
                    <div style="font-size: 12px; background: #FFFBEB; border-left: 3px solid #F59E0B; padding: 8px; margin-bottom: 12px; color: #92400E;">
                      <strong>Admin Feedback:</strong> ${sub.feedback}
                    </div>
                  ` : ''}

                  <form onsubmit="DashboardView.submitTask(event, '${app.id}', ${t.week_number})" style="display: flex; gap: 10px;">
                    <input type="url" id="file-url-${t.week_number}" class="form-input" placeholder="Paste Deliverable File URL (Google Drive / GitHub / Supabase Storage)..." value="${sub ? sub.file_url : ''}" required style="font-size: 13px; padding: 8px 12px;" />
                    <button type="submit" class="btn btn-primary btn-sm" style="white-space: nowrap;">
                      ${sub ? 'Re-submit' : 'Submit Task'}
                    </button>
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

  async submitTask(event, appId, weekNumber) {
    event.preventDefault();
    const fileUrl = document.getElementById(`file-url-${weekNumber}`).value.trim();

    try {
      Toast.show(`Submitting Week ${weekNumber} task...`, 'info');
      const res = await API.request('/api/submissions', {
        method: 'POST',
        body: {
          application_id: appId,
          week_number: weekNumber,
          file_url: fileUrl
        }
      });
      Toast.show(res.message, 'success');
      Modals.close();
      this.loadApplications();
    } catch (e) {
      Toast.show(e.message || 'Task submission failed.', 'error');
    }
  }
};
