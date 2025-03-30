<template>
  <div class="app-container">
    <header class="fixed-header">
      <h1>Lista de Operadoras</h1>
      <div class="search-container">
        <input
          v-model="termoBusca"
          @input="onInputChange"
          placeholder="Digite a razão social..."
          class="search-input"
        />
        <small v-if="carregando" class="loading-text">Buscando...</small>
      </div>
    </header>

    <main class="results-container">
      <div v-if="termoBusca && operadorasFiltradas.length" class="result-count">
        {{ operadorasFiltradas.length }} resultado(s) para "{{ termoBusca }}"
      </div>

      <div class="vertical-results">
        <div
          v-for="operadora in operadorasFiltradas"
          :key="operadora.registro_ans"
          class="operadora-card"
        >
          <div class="card-content">
            <h3>{{ operadora.razao_social }}</h3>
            <p><strong>Registro ANS:</strong> {{ operadora.registro_ans }}</p>
            <p><strong>CNPJ:</strong> {{ formatarCNPJ(operadora.cnpj) }}</p>
          </div>
        </div>
      </div>

      <div v-if="carregando" class="status-message">Carregando...</div>
      <div v-else-if="termoBusca && !operadorasFiltradas.length" class="status-message">
        Nenhuma operadora encontrada para "{{ termoBusca }}"
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      termoBusca: '',
      operadoras: [],
      carregando: false,
      timeout: null,
      apiUrl: import.meta.env.VITE_API_URL
    };
  },
  computed: {
    operadorasFiltradas() {
      if (!this.termoBusca) return [];
      return this.operadoras.filter(op =>
        op.razao_social.toLowerCase().includes(this.termoBusca.toLowerCase())
      );
    }
  },
  methods: {
    onInputChange() {
      clearTimeout(this.timeout);
      this.timeout = setTimeout(() => {
        this.handleBusca();
      }, 250);
    },
    
    async handleBusca() {
      if (!this.termoBusca.trim()) {
        this.operadoras = [];
        return;
      }

      this.carregando = true;

      try {
        const response = await axios.get(`${this.apiUrl}/api/operadoras/`, {
          params: {
            razao_social__icontains: this.termoBusca.trim(),
            page_size: 20
          }
        });
        
        this.operadoras = response.data.results;
      } catch (erro) {
        console.error('Erro na busca:', erro);
        this.operadoras = [];
      } finally {
        this.carregando = false;
      }
    },
    
    formatarCNPJ(cnpj) {
      if (!cnpj) return 'Não informado';
      return cnpj.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5');
    }
  }
};
</script>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

.fixed-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: #ffffff;
  padding: 15px 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  z-index: 100;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.fixed-header h1 {
  margin: 0 0 15px 0;
  font-size: 1.8rem;
  color: rgb(151, 16, 192);
}

.search-container {
  width: 100%;
  max-width: 600px;
}

.search-input {
  width: 100%;
  padding: 12px 20px;
  border: 1px solid #ddd;
  border-radius: 30px;
  font-size: 1rem;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.loading-text {
  display: block;
  text-align: center;
  margin-top: 8px;
  color: #666;
  font-size: 0.9rem;
}

.results-container {
  margin-top: 150px;
  padding: 20px;
  overflow-y: auto;
  height: calc(100vh - 150px);
}

.result-count {
  text-align: center;
  margin-bottom: 20px;
  color: #555;
  font-size: 1.1rem;
}

.vertical-results {
  display: flex;
  flex-direction: column;
  gap: 15px;
  max-width: 800px;
  margin: 0 auto;
}

.operadora-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.card-content h3 {
  margin: 0 0 10px 0;
  color: rgb(151, 16, 192);
  font-size: 1.2rem;
}

.card-content p {
  margin: 8px 0;
  color: #666;
  font-size: 0.9rem;
}

.card-content p strong {
  color: #444;
}

.status-message {
  text-align: center;
  padding: 30px;
  color: #666;
  font-size: 1.1rem;
}

.results-container::-webkit-scrollbar {
  width: 8px;
}

.results-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.results-container::-webkit-scrollbar-thumb {
  background: rgb(151, 16, 192);
  border-radius: 4px;
}

.results-container::-webkit-scrollbar-thumb:hover {
  background: rgb(151, 16, 192);
}
</style>