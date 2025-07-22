// Get DOM elements
const codeInput = document.getElementById('codeInput');
const fileInput = document.getElementById('fileInput');
const form = document.getElementById('codeForm');

// Clear file input if user types code
codeInput?.addEventListener('input', () => {
  if (fileInput?.value) fileInput.value = '';
});

// Clear textarea if user picks a file
fileInput?.addEventListener('change', () => {
  if (fileInput?.files.length > 0) codeInput.value = '';
});

// Prevent submission if no code and no file
form?.addEventListener('submit', (e) => {
  if (!codeInput?.value.trim() && !fileInput?.value) {
    e.preventDefault();
    alert('Please paste code or upload a .py file before generating flowchart.');
  }
});
