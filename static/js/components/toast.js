// Notification Toast Manager
const Toast = {
  show(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
      <span>${message}</span>
      <button onclick="this.parentElement.remove()" style="background:none; border:none; color:inherit; cursor:pointer; margin-left:12px;">&times;</button>
    `;

    container.appendChild(toast);

    setTimeout(() => {
      if (toast.parentElement) {
        toast.remove();
      }
    }, 4000);
  }
};
