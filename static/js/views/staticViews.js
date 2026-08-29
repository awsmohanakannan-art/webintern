// Static Informational Pages Renderer
const StaticViews = {
  renderAbout() {
    const container = document.getElementById('app-view');
    if (!container) return;

    container.innerHTML = `
      <section class="section-padding" style="background-color: var(--color-gray-bg);">
        <div class="container" style="max-width: 900px;">
          <div style="background: white; border-radius: var(--radius-lg); padding: 48px; border: 1px solid var(--color-border);">
            <span class="badge-sector" style="margin-bottom: 12px; display: inline-block;">ABOUT WEB INTERN</span>
            <h1 style="font-size: 38px; color: var(--color-blue-dark); margin-bottom: 20px;">Democratizing Practical Career Experience</h1>
            <p style="font-size: 16px; color: var(--color-gray-text); line-height: 1.8; margin-bottom: 24px;">
              Web Intern is a virtual internship platform designed to bridge the gap between academic education and real-world software engineering, data analytics, product design, and performance marketing skills.
            </p>

            <h3 style="font-size: 22px; color: var(--color-blue-dark); margin-bottom: 12px;">Our Mission</h3>
            <p style="font-size: 15px; color: var(--color-gray-text); line-height: 1.7; margin-bottom: 24px;">
              We believe every student deserves access to structured, hands-on industry project tasks without financial barriers. By providing free sector-specific internship simulations, instant offer letters, expert feedback, and verifiable certificates, we empower candidates to stand out in the job market.
            </p>

            <div style="margin-top: 32px;">
              <a href="#/internships" class="btn btn-primary btn-lg">Explore Available Programs →</a>
            </div>
          </div>
        </div>
      </section>
    `;
    if (window.feather) feather.replace();
  },

  renderContact() {
    const container = document.getElementById('app-view');
    if (!container) return;

    container.innerHTML = `
      <section class="section-padding" style="background-color: var(--color-gray-bg);">
        <div class="container" style="max-width: 600px;">
          <div style="background: white; border-radius: var(--radius-lg); padding: 40px 32px; border: 1px solid var(--color-border);">
            <h1 style="font-size: 32px; color: var(--color-blue-dark); margin-bottom: 8px;">Contact Support</h1>
            <p style="color: var(--color-gray-text); font-size: 14px; margin-bottom: 28px;">Have questions about your virtual internship or certificate verification? Send us a message.</p>

            <form id="contact-form">
              <div class="form-group">
                <label class="form-label">Your Name</label>
                <input type="text" id="contact-name" class="form-input" placeholder="Enter your full name" required />
              </div>

              <div class="form-group">
                <label class="form-label">Email Address</label>
                <input type="email" id="contact-email" class="form-input" placeholder="you@example.com" required />
              </div>

              <div class="form-group">
                <label class="form-label">Message</label>
                <textarea id="contact-message" class="form-input" rows="4" placeholder="How can we help you?" required></textarea>
              </div>

              <button type="submit" class="btn btn-primary btn-full btn-lg">Send Message</button>
            </form>
          </div>
        </div>
      </section>
    `;

    if (window.feather) feather.replace();

    document.getElementById('contact-form')?.addEventListener('submit', async (e) => {
      e.preventDefault();
      const name = document.getElementById('contact-name').value.trim();
      const email = document.getElementById('contact-email').value.trim();
      const message = document.getElementById('contact-message').value.trim();

      try {
        const res = await API.request('/api/contact', {
          method: 'POST',
          body: { name, email, message }
        });
        Toast.show(res.message, 'success');
        e.target.reset();
      } catch (err) {
        Toast.show(err.message, 'error');
      }
    });
  },

  renderPrivacy() {
    const container = document.getElementById('app-view');
    if (!container) return;

    container.innerHTML = `
      <section class="section-padding" style="background-color: var(--color-gray-bg);">
        <div class="container" style="max-width: 800px;">
          <div style="background: white; border-radius: var(--radius-lg); padding: 48px; border: 1px solid var(--color-border);">
            <h1 style="font-size: 32px; color: var(--color-blue-dark); margin-bottom: 16px;">Privacy Policy & Terms of Service</h1>
            <p style="color: var(--color-gray-text); font-size: 14px; margin-bottom: 24px;">Last updated: August 2026</p>

            <h3 style="font-size: 18px; color: var(--color-blue-dark); margin-bottom: 8px;">1. Information We Collect</h3>
            <p style="font-size: 14px; color: var(--color-gray-text); line-height: 1.6; margin-bottom: 20px;">
              We collect your name, email address, mobile number, and submitted task deliverable files to manage your internship participation, generate offer letters, and issue completion certificates.
            </p>

            <h3 style="font-size: 18px; color: var(--color-blue-dark); margin-bottom: 8px;">2. User Consent & Marketing Preferences</h3>
            <p style="font-size: 14px; color: var(--color-gray-text); line-height: 1.6; margin-bottom: 20px;">
              By checking the terms agreement upon registration, you authorize Web Intern to issue credentials and store program progress. Marketing emails are separate and opt-in only.
            </p>

            <h3 style="font-size: 18px; color: var(--color-blue-dark); margin-bottom: 8px;">3. Data Security</h3>
            <p style="font-size: 14px; color: var(--color-gray-text); line-height: 1.6;">
              All credentials and JWT session tokens are stored using industry-standard hashing protocols (Bcrypt & SHA-256).
            </p>
          </div>
        </div>
      </section>
    `;
    if (window.feather) feather.replace();
  }
};
