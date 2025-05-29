/** @type {import('tailwindcss').Config} */
module.exports = {
  // Pastikan Tailwind memindai file-file ini untuk kelas CSS
  content: [
    "./templates/**/*.html", // Pindai semua file HTML di folder templates
    "./static/js/**/*.js",   // Pindai semua file JS di folder static/js (jika Anda pakai JS untuk menambahkan elemen dengan kelas Tailwind)
    // Tambahkan path lain jika Anda punya komponen HTML/JS di luar ini
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}