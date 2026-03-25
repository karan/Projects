import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        bumpa: {
          green: "#00A86B",
          "green-dark": "#008A57",
          "green-light": "#E6F7F1",
          "green-mid": "#00C47E",
        },
      },
    },
  },
  plugins: [],
};

export default config;
