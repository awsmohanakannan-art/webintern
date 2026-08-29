// Explore Internships & Sectors View Renderer
const ExploreView = {
  async renderInternships(sectorSlug = null) {
    const container = document.getElementById('app-view');
    if (!container) return;

    container.innerHTML = `
      <section class="section-padding" style="background-color: var(--color-gray-bg);">
        <div class="container">
          <div style="text-align: center; max-width: 700px; margin: 0 auto 36px auto;">
            <h1 style="font-size: 38px; color: var(--color-blue-dark); margin-bottom: 12px;">Browse Virtual Internships</h1>
            <p style="color: var(--color-gray-text);">Explore sector-based 4-week internship programs, submit weekly deliverables, and earn verified industry credentials.</p>
          </div>

          <!-- Filter & Search Controls -->
          <div style="background: var(--color-white); border-radius: var(--radius-lg); padding: 20px; border: 1px solid var(--color-border); margin-bottom: 36px; display: flex; gap: 16px; flex-wrap: wrap; align-items: center; justify-content: space-between;">
            <div style="flex-grow: 1; min-width: 260px; display: flex; align-items: center; gap: 10px; background: var(--color-gray-bg); border: 1px solid var(--color-border); padding: 10px 16px; border-radius: var(--radius-full);">
              <i data-feather="search" style="color: var(--color-gray-text); width: 18px;"></i>
              <input type="text" id="explore-search-input" class="mobile-search-input" placeholder="Search by title or keyword..." />
            </div>

            <div style="display: flex; gap: 12px; align-items: center;" id="sector-filter-tabs">
              <!-- Sector filter buttons dynamically populated -->
            </div>
          </div>

          <div class="cards-grid" id="explore-internships-grid">
            <div style="grid-column: 1/-1; text-align: center; padding: 40px;">Loading internships...</div>
          </div>
        </div>
      </section>
    `;

    if (window.feather) feather.replace();

    await this.loadFilters(sectorSlug);
    await this.fetchInternships(sectorSlug);

    const searchInput = document.getElementById('explore-search-input');
    if (searchInput) {
      searchInput.addEventListener('input', (e) => {
        this.fetchInternships(sectorSlug, e.target.value);
      });
    }
  },

  async loadFilters(activeSectorSlug) {
    try {
      const res = await API.request('/api/sectors');
      const tabs = document.getElementById('sector-filter-tabs');
      if (res.sectors && tabs) {
        let html = `<button class="btn btn-sm ${!activeSectorSlug ? 'btn-primary' : 'btn-outline'}" onclick="window.location.hash='#/internships'">All</button>`;
        html += res.sectors.map(sec => `
          <button class="btn btn-sm ${activeSectorSlug === sec.slug ? 'btn-primary' : 'btn-outline'}" onclick="window.location.hash='#/sector/${sec.slug}'">${sec.name}</button>
        `).join('');
        tabs.innerHTML = html;
      }
    } catch (e) {
      console.warn("Filters load error:", e);
    }
  },

  async fetchInternships(sectorSlug = null, searchQuery = '') {
    try {
      let url = '/api/internships?';
      if (sectorSlug) url += `sector=${encodeURIComponent(sectorSlug)}&`;
      if (searchQuery) url += `search=${encodeURIComponent(searchQuery)}`;

      const res = await API.request(url);
      const grid = document.getElementById('explore-internships-grid');
      if (res.internships && grid) {
        if (res.internships.length === 0) {
          grid.innerHTML = `<div style="grid-column:1/-1; text-align:center; padding: 40px; color: var(--color-gray-text);">No internships match your filter criteria.</div>`;
          return;
        }

        grid.innerHTML = res.internships.map(item => `
          <div class="card">
            <div class="card-header">
              <span class="badge-sector">${item.sector_name}</span>
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
      console.error("Fetch internships error:", e);
    }
  },

  async renderSectors() {
    const container = document.getElementById('app-view');
    if (!container) return;

    container.innerHTML = `
      <section class="section-padding" style="background-color: var(--color-gray-bg);">
        <div class="container">
          <div style="text-align: center; max-width: 600px; margin: 0 auto 48px auto;">
            <h1 style="font-size: 38px; color: var(--color-blue-dark); margin-bottom: 12px;">All Sector Tracks</h1>
            <p style="color: var(--color-gray-text);">Choose a sector domain to view all virtual internship programs available.</p>
          </div>

          <div class="cards-grid" id="all-sectors-grid">
            <div style="grid-column: 1/-1; text-align: center; padding: 40px;">Loading sectors...</div>
          </div>
        </div>
      </section>
    `;

    try {
      const res = await API.request('/api/sectors');
      const grid = document.getElementById('all-sectors-grid');
      if (res.sectors && grid) {
        grid.innerHTML = res.sectors.map(sec => `
          <div class="card">
            <div style="width: 56px; height: 56px; border-radius: 14px; background: var(--color-blue-light); color: var(--color-primary-blue); display:flex; align-items:center; justify-content:center; margin-bottom: 16px;">
              <i data-feather="${sec.icon_url || 'grid'}" style="width: 28px; height: 28px;"></i>
            </div>
            <h3 class="card-title">${sec.name}</h3>
            <p class="card-desc">${sec.description}</p>
            <div class="card-footer">
              <span class="duration-info">${sec.internships_count || 1} Program(s)</span>
              <a href="#/sector/${sec.slug}" class="btn btn-outline btn-sm">Explore Sector →</a>
            </div>
          </div>
        `).join('');
        if (window.feather) feather.replace();
      }
    } catch (e) {
      console.error("All sectors load error:", e);
    }
  }
};
