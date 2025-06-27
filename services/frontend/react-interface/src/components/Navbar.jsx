import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const location = useLocation();
  const { user, logout } = useAuth();

  const navItems = [
    { path: "/", label: "Accueil" },
    { path: "/upload", label: "Upload" },
    { path: "/result", label: "Résultat" },
  ];

  return (
    <nav className="bg-white shadow-md px-6 py-4 flex justify-between items-center">
      <ul className="flex gap-6">
        {navItems.map(({ path, label }) => (
          <li key={path}>
            <Link
              to={path}
              className={`text-lg font-medium transition-colors ${
                location.pathname === path
                  ? "text-indigo-600 border-b-2 border-indigo-600"
                  : "text-gray-600 hover:text-indigo-600"
              }`}
            >
              {label}
            </Link>
          </li>
        ))}
      </ul>
      {user && (
        <div className="flex items-center gap-4">
          <span className="text-gray-700 font-medium">👤 {user.name}</span>
          <button
            onClick={logout}
            className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600"
          >
            Déconnexion
          </button>
        </div>
      )}
    </nav>
  );
}