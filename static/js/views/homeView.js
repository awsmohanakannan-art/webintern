// Homepage View Renderer
const HomeView = {
  async render() {
    const container = document.getElementById('app-view');
    if (!container) return;

    container.innerHTML = `
      <!-- Hero Section -->
      <section class="hero-section">
        <div class="hero-overlay-grid"></div>
        <div class="container hero-content">
          <div class="badge-pill-top">
            <i data-feather="award" style="width: 14px; height: 14px;"></i>
            VIRTUAL INTERNSHIP PLATFORM
          </div>

          <h1 class="hero-title">
            Build Real Industry Skills with <span class="accent-word">Virtual Internships</span>
          </h1>

          <p class="hero-description">
            Apply instantly to top industry programs, receive an official offer letter, submit weekly project task deliverables, get expert evaluation, and earn a verified certificate.
          </p>

          <div class="hero-cta-group">
            <a href="#/internships" class="btn btn-primary btn-lg">
              Start Free Internship
              <i data-feather="arrow-right" style="width: 18px; height: 18px;"></i>
            </a>
            <a href="#how-it-works-section" class="btn btn-outline btn-white btn-lg">
              <i data-feather="play-circle" style="width: 18px; height: 18px;"></i>
              How It Works
            </a>
          </div>

          <div class="hero-trust-badge">
            <i data-feather="shield-check" style="color: var(--color-accent-blue); width: 18px; height: 18px;"></i>
            100% Verified Program · Direct Industry Project Experience
          </div>

          <div class="hero-feature-pills">
            <div class="feature-pill">
              <i data-feather="check" style="color: var(--color-accent-blue); width: 14px;"></i>
              Begin in 2 Minutes
            </div>
            <div class="feature-pill">
              <i data-feather="check" style="color: var(--color-accent-blue); width: 14px;"></i>
              100% Free to Start
            </div>
            <div class="feature-pill">
              <i data-feather="check" style="color: var(--color-accent-blue); width: 14px;"></i>
              Self-Paced Modules
            </div>
          </div>

          <div class="hero-callout-bar">
            <i data-feather="file-text" style="color: var(--color-accent-blue); width: 18px;"></i>
            <span>Get your Official Letter of Experience instantly upon applying</span>
          </div>
        </div>
      </section>

      <!-- Section 4A: Stats Bar Section (White background, sits below hero) -->
      <section class="stats-section">
        <div class="container">
          <div class="stats-eyebrow">EXPERIENCE & IMPACT</div>

          <!-- 2x2 grid on mobile, single row on desktop -->
          <div class="stats-grid" id="home-stats-grid">
            <div class="stat-card">
              <div class="stat-icon-badge tint-peach">
                <i data-feather="users" style="width: 36px; height: 36px;"></i>
              </div>
              <div class="stat-number">1 Lakh+</div>
              <div class="stat-label">Happy Users<br/>Enrolled Platform Students</div>
            </div>
            <div class="stat-card">
              <div class="stat-icon-badge tint-peach">
                <i data-feather="target" style="width: 36px; height: 36px;"></i>
              </div>
              <div class="stat-number">97%</div>
              <div class="stat-label">Job-Role Match Rate<br/>Industry Readiness</div>
            </div>
            <div class="stat-card">
              <div class="stat-icon-badge tint-yellow">
                <i data-feather="trending-up" style="width: 36px; height: 36px;"></i>
              </div>
              <div class="stat-number">98%</div>
              <div class="stat-label">Skill Improvement<br/>Project Completion Success</div>
            </div>
            <div class="stat-card">
              <div class="stat-icon-badge tint-yellow">
                <i data-feather="award" style="width: 36px; height: 36px;"></i>
              </div>
              <div class="stat-number">Web Intern</div>
              <div class="stat-label">Verified Program<br/>Credential System</div>
            </div>
          </div>

          <div class="stats-bottom-pill">
            <span>OUR INTERNS. REAL IMPACT.</span>
          </div>
        </div>
      </section>

      <!-- Marquee Ticker -->
      <div class="marquee-container">
        <div class="marquee-content">
          <div class="marquee-item"><i data-feather="check-circle" style="width: 16px;"></i> Instant Offer Letter</div>
          <div class="marquee-item"><i data-feather="check-circle" style="width: 16px;"></i> Weekly Task Submissions</div>
          <div class="marquee-item"><i data-feather="check-circle" style="width: 16px;"></i> Expert Evaluation & Feedback</div>
          <div class="marquee-item"><i data-feather="check-circle" style="width: 16px;"></i> Verified Certificates</div>
          <div class="marquee-item"><i data-feather="check-circle" style="width: 16px;"></i> 100% Free Virtual Internships</div>
          <div class="marquee-item"><i data-feather="check-circle" style="width: 16px;"></i> Instant Offer Letter</div>
          <div class="marquee-item"><i data-feather="check-circle" style="width: 16px;"></i> Weekly Task Submissions</div>
          <div class="marquee-item"><i data-feather="check-circle" style="width: 16px;"></i> Expert Evaluation & Feedback</div>
          <div class="marquee-item"><i data-feather="check-circle" style="width: 16px;"></i> Verified Certificates</div>
        </div>
      </div>

      <!-- Sectors Grid Section -->
      <section class="section-padding" style="background-color: var(--color-gray-bg);">
        <div class="container">
          <div style="text-align: center; max-width: 600px; margin: 0 auto 48px auto;">
            <h2 style="font-size: 32px; color: var(--color-blue-dark); margin-bottom: 12px;">Explore Internship Sectors</h2>
            <p style="color: var(--color-gray-text);">Select your domain of interest to start your hands-on virtual internship program today.</p>
          </div>

          <div class="cards-grid" id="home-sectors-grid">
            <!-- Dynamically populated -->
            <div style="text-align:center; padding: 20px; grid-column: 1/-1;">Loading sectors...</div>
          </div>

          <div style="text-align: center; margin-top: 36px;">
            <a href="#/sectors" class="btn btn-outline">View All Sectors →</a>
          </div>
        </div>
      </section>

      <!-- Featured Internships Section -->
      <section class="section-padding" style="background-color: var(--color-white);">
        <div class="container">
          <div style="display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 48px; flex-wrap: wrap; gap: 16px;">
            <div>
              <span style="color: var(--color-accent-blue); font-weight: 700; text-transform: uppercase; font-size: 13px; letter-spacing: 1px;">POPULAR PROGRAMS</span>
              <h2 style="font-size: 32px; color: var(--color-blue-dark); margin-top: 4px;">Featured Virtual Internships</h2>
            </div>
            <a href="#/internships" class="btn btn-outline btn-sm">Explore All Internships →</a>
          </div>

          <div class="cards-grid" id="home-featured-grid">
            <!-- Dynamically populated -->
          </div>
        </div>
      </section>

      <!-- How It Works Section -->
      <section id="how-it-works-section" class="section-padding" style="background-color: var(--color-gray-bg);">
        <div class="container">
          <div style="text-align: center; max-width: 600px; margin: 0 auto 56px auto;">
            <span style="color: var(--color-accent-blue); font-weight: 700; text-transform: uppercase; font-size: 13px; letter-spacing: 1px;">SIMPLE STEP-BY-STEP PROCESS</span>
            <h2 style="font-size: 32px; color: var(--color-blue-dark); margin-top: 6px;">How Web Intern Works</h2>
          </div>

          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 24px;">
            <div style="background: var(--color-white); border-radius: var(--radius-lg); padding: 32px 24px; border: 1px solid var(--color-border); text-align: center;">
              <div style="width: 56px; height: 56px; border-radius: 50%; background: var(--color-blue-light); color: var(--color-primary-blue); font-weight: 800; font-size: 20px; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px auto;">1</div>
              <h3 style="font-size: 18px; color: var(--color-blue-dark); margin-bottom: 10px;">Select & Apply</h3>
              <p style="font-size: 14px; color: var(--color-gray-text);">Browse sectors and apply instantly to your preferred internship with zero fee requirements.</p>
            </div>

            <div style="background: var(--color-white); border-radius: var(--radius-lg); padding: 32px 24px; border: 1px solid var(--color-border); text-align: center;">
              <div style="width: 56px; height: 56px; border-radius: 50%; background: var(--color-blue-light); color: var(--color-primary-blue); font-weight: 800; font-size: 20px; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px auto;">2</div>
              <h3 style="font-size: 18px; color: var(--color-blue-dark); margin-bottom: 10px;">Get Offer Letter</h3>
              <p style="font-size: 14px; color: var(--color-gray-text);">Receive an automated, official Internship Offer Letter directly in your inbox and portal.</p>
            </div>

            <div style="background: var(--color-white); border-radius: var(--radius-lg); padding: 32px 24px; border: 1px solid var(--color-border); text-align: center;">
              <div style="width: 56px; height: 56px; border-radius: 50%; background: var(--color-blue-light); color: var(--color-primary-blue); font-weight: 800; font-size: 20px; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px auto;">3</div>
              <h3 style="font-size: 18px; color: var(--color-blue-dark); margin-bottom: 10px;">Submit Weekly Tasks</h3>
              <p style="font-size: 14px; color: var(--color-gray-text);">Execute real project briefs week by week, uploading deliverables for admin evaluation.</p>
            </div>

            <div style="background: var(--color-white); border-radius: var(--radius-lg); padding: 32px 24px; border: 1px solid var(--color-border); text-align: center;">
              <div style="width: 56px; height: 56px; border-radius: 50%; background: var(--color-blue-light); color: var(--color-primary-blue); font-weight: 800; font-size: 20px; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px auto;">4</div>
              <h3 style="font-size: 18px; color: var(--color-blue-dark); margin-bottom: 10px;">Earn Certificate</h3>
              <p style="font-size: 14px; color: var(--color-gray-text);">On final review approval, download your verified certificate of completion instantly.</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Video / Interactive Demo Section -->
      <section class="section-padding" style="background-color: var(--color-white);">
        <div class="container">
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 48px; align-items: center;">
            <div>
              <span style="color: var(--color-accent-blue); font-weight: 700; text-transform: uppercase; font-size: 13px; letter-spacing: 1px;">STUDENT WORKSPACE DEMO</span>
              <h2 style="font-size: 36px; color: var(--color-blue-dark); margin: 12px 0 20px 0;">Experience the Platform in Action</h2>
              <p style="color: var(--color-gray-text); font-size: 16px; line-height: 1.6; margin-bottom: 24px;">
                Our intuitive workspace makes completing virtual internships seamless. Track progress bars, access task briefs, submit files, and communicate with evaluators effortlessly.
              </p>
              <ul style="list-style: none; display: flex; flex-direction: column; gap: 14px; margin-bottom: 32px;">
                <li style="display: flex; align-items: center; gap: 10px; font-weight: 600; color: var(--color-blue-dark);">
                  <i data-feather="check-circle" style="color: var(--color-accent-blue);"></i> Clear weekly task objectives and deliverables list
                </li>
                <li style="display: flex; align-items: center; gap: 10px; font-weight: 600; color: var(--color-blue-dark);">
                  <i data-feather="check-circle" style="color: var(--color-accent-blue);"></i> Instant feedback notification on every submission
                </li>
                <li style="display: flex; align-items: center; gap: 10px; font-weight: 600; color: var(--color-blue-dark);">
                  <i data-feather="check-circle" style="color: var(--color-accent-blue);"></i> One-click digital PDF certificate generation
                </li>
              </ul>
              <a href="#/register" class="btn btn-primary btn-lg">Join Platform Now →</a>
            </div>

            <div style="position: relative; border-radius: var(--radius-lg); overflow: hidden; box-shadow: var(--shadow-xl); border: 1px solid var(--color-border); background: #000; aspect-ratio: 16/9; display: flex; align-items: center; justify-content: center;">
              <iframe width="100%" height="100%" src="https://www.youtube.com/embed/dQw4w9WgXcQ" title="Platform Walkthrough" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="border:none;"></iframe>
            </div>
          </div>
        </div>
      </section>

      <!-- Testimonials Carousel Section -->
      <section class="section-padding" style="background-color: var(--color-gray-bg);">
        <div class="container">
          <div style="text-align: center; max-width: 600px; margin: 0 auto 48px auto;">
            <span style="color: var(--color-accent-blue); font-weight: 700; text-transform: uppercase; font-size: 13px; letter-spacing: 1px;">STUDENT REVIEWS</span>
            <h2 style="font-size: 32px; color: var(--color-blue-dark); margin-top: 6px;">What Our Interns Say</h2>
          </div>

          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px;" id="home-testimonials-grid">
            <!-- Dynamically populated -->
          </div>
        </div>
      </section>

      <!-- Certificate Upgrade Teaser -->
      <section class="section-padding" style="background-color: var(--color-white);">
        <div class="container">
          <div style="background: linear-gradient(135deg, var(--color-blue-light) 0%, #FFFFFF 100%); border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: 48px; display: grid; grid-template-columns: 2fr 1fr; gap: 40px; align-items: center;">
            <div>
              <span class="badge-sector" style="margin-bottom: 12px; display: inline-block;">OPTIONAL PAID ADD-ON</span>
              <h2 style="font-size: 32px; color: var(--color-blue-dark); margin-bottom: 16px;">Upgrade to Verified & Printed Certificate</h2>
              <p style="color: var(--color-gray-text); line-height: 1.6; margin-bottom: 20px;">
                Enhance your resume credibility with an official tamper-proof QR code verified digital credential and a high-quality physical hardcopy certificate shipped directly to your address.
              </p>
              <div style="display: flex; gap: 20px; align-items: center;">
                <span style="font-size: 36px; font-weight: 900; color: var(--color-primary-blue);" id="product-price-display">₹499</span>
                <span style="color: var(--color-gray-text); font-size: 14px;">One-time optional upgrade fee via Razorpay</span>
              </div>
            </div>
            <div style="text-align: center;">
              <a href="#/register" class="btn btn-primary btn-lg btn-full">Get Started Free</a>
              <p style="font-size: 12px; color: var(--color-gray-text); margin-top: 10px;">100% Free to complete internship & get standard digital certificate</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Newsletter Section -->
      <section class="section-padding" style="background-color: var(--color-blue-dark); color: var(--color-white);">
        <div class="container" style="text-align: center; max-width: 680px;">
          <h2 style="font-size: 32px; color: var(--color-white); margin-bottom: 12px;">Stay Updated with New Internship Sectors</h2>
          <p style="color: #DCE6F5; margin-bottom: 32px;">Subscribe to receive weekly career tips, newly launched virtual internship tracks, and industry guidance.</p>

          <form id="home-newsletter-form" style="display: flex; gap: 12px; max-width: 500px; margin: 0 auto; flex-wrap: wrap;">
            <input type="email" id="newsletter-email" class="form-input" placeholder="Enter your email address..." required style="flex-grow: 1; border-radius: var(--radius-full); padding-left: 20px;" />
            <button type="submit" class="btn btn-primary" style="background-color: var(--color-accent-blue); border-color: var(--color-accent-blue);">Subscribe</button>
          </form>
        </div>
      </section>
    `;

    if (window.feather) feather.replace();

    // Fetch dynamic content
    this.loadStats();
    this.loadSectors();
    this.loadFeatured();
    this.loadTestimonials();

    // Bind newsletter form
    const form = document.getElementById('home-newsletter-form');
    if (form) {
      form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('newsletter-email').value;
        try {
          const res = await API.request('/api/newsletter', {
            method: 'POST',
            body: { email }
          });
          Toast.show(res.message, 'success');
          form.reset();
        } catch (err) {
          Toast.show(err.message, 'error');
        }
      });
    }
  },

  async loadStats() {
    try {
      const res = await API.request('/api/site-stats');
      const grid = document.getElementById('home-stats-grid');
      if (res.stats && res.stats.length > 0 && grid) {
        grid.innerHTML = res.stats.map((s, idx) => {
          const tintClass = idx % 4 < 2 ? 'tint-peach' : 'tint-yellow';
          const iconName = s.icon_name || 'award';
          return `
            <div class="stat-card">
              <div class="stat-icon-badge ${tintClass}">
                <i data-feather="${iconName}" style="width: 36px; height: 36px;"></i>
              </div>
              <div class="stat-number">${s.value}</div>
              <div class="stat-label">${s.label}</div>
            </div>
          `;
        }).join('');
        if (window.feather) feather.replace();
      }
    } catch (e) {
      console.warn("Stats load fallback:", e);
    }
  },

  async loadSectors() {
    try {
      const res = await API.request('/api/sectors');
      const grid = document.getElementById('home-sectors-grid');
      if (res.sectors && grid) {
        grid.innerHTML = res.sectors.map(sec => `
          <a href="#/sector/${sec.slug}" class="card" style="text-decoration:none;">
            <div style="width: 48px; height: 48px; border-radius: 12px; background: var(--color-blue-light); color: var(--color-primary-blue); display:flex; align-items:center; justify-content:center; margin-bottom: 16px;">
              <i data-feather="${sec.icon_url || 'grid'}" style="width: 24px; height: 24px;"></i>
            </div>
            <h3 class="card-title">${sec.name}</h3>
            <p class="card-desc">${sec.description || 'Explore virtual project modules and skill assessments.'}</p>
            <div class="card-footer">
              <span class="duration-info">${sec.internships_count || 1} Active Track(s)</span>
              <span style="color: var(--color-accent-blue); font-weight:700;">Explore →</span>
            </div>
          </a>
        `).join('');
        if (window.feather) feather.replace();
      }
    } catch (e) {
      console.warn("Sectors load error:", e);
    }
  },

  async loadFeatured() {
    const grid = document.getElementById('home-featured-grid');
    if (grid) {
      grid.innerHTML = ExploreView.getSkeletonCardsHTML ? ExploreView.getSkeletonCardsHTML().slice(0, 3) : '<div style="grid-column:1/-1; text-align:center; padding:20px;">Loading featured programs...</div>';
    }

    try {
      const res = await API.request('/api/internships?featured=true&per_page=6');
      if (res.internships && grid) {
        if (res.internships.length === 0) {
          grid.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 20px; color: var(--color-gray-text);">No featured internships available right now.</div>`;
          return;
        }

        grid.innerHTML = res.internships.map(item => `
          <div class="card">
            <div class="card-header">
              <span class="badge-sector">${item.sector_name || 'Virtual Track'}</span>
              <span class="badge-mode">${item.mode || 'Virtual'}</span>
            </div>
            <h3 class="card-title">${item.title}</h3>
            <p class="card-desc">${item.short_description}</p>
            <div class="card-footer">
              <span class="duration-info">
                <i data-feather="clock" style="width: 14px;"></i>
                ${item.duration_weeks} Weeks
              </span>
              <a href="#/internship/${item.slug}" class="btn btn-outline btn-sm">View Details</a>
            </div>
          </div>
        `).join('');
        if (window.feather) feather.replace();
      }
    } catch (e) {
      console.warn("Featured load warning:", e);
      if (grid) {
        grid.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 20px; color: var(--color-gray-text);">Unable to load featured programs.</div>`;
      }
    }
  },

  async loadTestimonials() {
    try {
      const res = await API.request('/api/testimonials');
      const grid = document.getElementById('home-testimonials-grid');
      if (res.testimonials && grid) {
        grid.innerHTML = res.testimonials.map(t => `
          <div style="background: var(--color-white); border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: 24px; box-shadow: var(--shadow-sm);">
            <div style="color: #F59E0B; margin-bottom: 12px; font-size: 18px;">★★★★★</div>
            <p style="font-size: 14px; color: var(--color-gray-text); line-height: 1.6; margin-bottom: 20px; font-style: italic;">"${t.quote}"</p>
            <div style="display: flex; align-items: center; gap: 12px;">
              <div style="width: 44px; height: 44px; border-radius: 50%; background: var(--color-blue-light); color: var(--color-primary-blue); display:flex; align-items:center; justify-content:center; font-weight:700;">
                ${t.name.charAt(0)}
              </div>
              <div>
                <h4 style="font-size: 15px; color: var(--color-blue-dark); margin:0;">${t.name}</h4>
                <span style="font-size: 12px; color: var(--color-gray-text);">${t.role}</span>
              </div>
            </div>
          </div>
        `).join('');
      }
    } catch (e) {
      console.warn("Testimonials load error:", e);
    }
  }
};
