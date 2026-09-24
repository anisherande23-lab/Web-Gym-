const app = require('./app');

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`====================================================`);
  console.log(` 🚀 Cosarc Dynamic Web Application Running!`);
  console.log(` 📍 Local URL: http://localhost:${PORT}`);
  console.log(` 🏥 Health Check: http://localhost:${PORT}/health`);
  console.log(` 🌐 API Endpoint: http://localhost:${PORT}/api/contracts`);
  console.log(`====================================================`);
});
