import { config } from '@fisch0920/config/eslint'
import { globalIgnores } from 'eslint/config'

export default [
  ...config,
  globalIgnores(['out', 'dist', 'examples']),
  // No `any` and no `as` type assertions (vh-framework-corpus/development_standards.md → "Type-checked on
  // every edit", Isaac 2026-10-26); `as const` stays allowed. WARN first: existing ones are fixed when
  // their file is touched. ban-ts-comment already comes from @fisch0920/config (error).
  {
    files: ['**/*.ts', '**/*.tsx'],
    rules: {
      '@typescript-eslint/no-explicit-any': 'warn',
      '@typescript-eslint/consistent-type-assertions': [
        'warn',
        { assertionStyle: 'never' }
      ]
    }
  }
]
