/** @type {import('eslint').Linter.Config} */
module.exports = {
    extends: [
        'sznm/react',
        'plugin:react/jsx-runtime',
        'eslint:recommended',
        'plugin:react/recommended',
    ],
    env: {
        browser: true,
    },
};
