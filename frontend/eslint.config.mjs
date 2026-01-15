import nextPlugin from 'eslint-config-next';

const eslintConfig = [
  {
    ignores: ['.next/**', 'node_modules/**', 'out/**', 'build/**', 'dist/**'],
  },
  ...nextPlugin,
  {
    rules: {
      'react/react-in-jsx-scope': 'off',
      '@next/next/no-img-element': 'warn',
      'no-console': ['warn', { allow: ['warn', 'error'] }],
    },
  },
];

export default eslintConfig;
