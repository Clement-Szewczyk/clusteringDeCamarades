<style scoped>
h1 {
  color: #2c3e50;
  margin-bottom: 20px;
}

button {
  background-color: #3498db;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  margin-bottom: 20px;
  transition: background-color 0.2s;
}

button:hover {
  background-color: #2980b9;
}

.lists-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-top: 30px;
}

.half-width {
  flex: 1;
  min-width: 300px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 20px;
}

.half-width h1 {
  font-size: 1.5rem;
  margin-top: 0;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

li {
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}

.loading, .error, .no-data {
  padding: 15px;
  margin: 10px 0;
  border-radius: 4px;
  text-align: center;
}

.loading {
  background-color: #f5f5f5;
  color: #666;
}

.error {
  background-color: #fadbd8;
  color: #c0392b;
}

.no-data {
  background-color: #f9f9f9;
  color: #7f8c8d;
  font-style: italic;
}
</style>