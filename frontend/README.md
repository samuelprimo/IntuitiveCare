## 🔍 Teste de API - Funcionalidades

### 🛠️ Tarefas Implementadas
1. **Integração com Backend**:
   - Conexão com API Django via `axios`
   - Variável de ambiente `VITE_API_URL` configurada na .env
```ini
# Arquivo: frontend/.env
VITE_API_URL=http://localhost:8000
```

2. **Busca de Operadoras**:
   - Campo de busca com debounce (250ms)
   - Filtro por razão social (case insensitive)
   - Paginação (20 resultados por requisição)

3. **Visualização de Resultados**:
   - Cards responsivos com informações essenciais
   - Formatação automática de CNPJ
   - Feedback visual durante carregamento

## 💻 Componente Principal (`OperadorasView.vue`)

- Setup

```sh
npm install
```

- Compile 

```sh
npm run dev
```

