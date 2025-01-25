import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

import React from 'react';

const Header = () => <header className="p-4 bg-blue-500 text-white">Header</header>;

const Sidebar = () => (
  <aside className="p-4 bg-gray-200 w-1/4">Sidebar</aside>
);

const MainContent = () => (
  <main className="p-4 flex-1">
    <section>
      <h1 className="text-xl font-bold">Main page</h1>
      <p>Home Page</p>
    </section>
  </main>
);

const Footer = () => <footer className="p-4 bg-blue-500 text-white">Footer</footer>;

const Page = () => (
  <div className="flex flex-col min-h-screen">
    <Header />
    <div className="flex flex-1">
      <Sidebar />
      <MainContent />
    </div>
    <Footer />
  </div>
);

export default Page;
