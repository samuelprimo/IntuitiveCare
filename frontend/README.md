## 🔍 Teste de API - Funcionalidades

### 🛠️ Tarefas Implementadas
1. **Integração com Backend**:
   - Conexão com API Django via `axios`
   - Variável de ambiente `VITE_API_URL` configurada na .env

2. **Busca de Operadoras**:
   - Campo de busca com debounce (250ms)
   - Filtro por razão social (case insensitive)
   - Paginação (20 resultados por requisição)

3. **Visualização de Resultados**:
   - Cards responsivos com informações essenciais
   - Formatação automática de CNPJ
   - Feedback visual durante carregamento

## 💻 Componente Principal (`OperadorasView.vue`)

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```
