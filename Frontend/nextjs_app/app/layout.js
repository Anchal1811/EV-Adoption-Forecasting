import "./globals.scss";
import Sidebar from "@/components/Sidebar";

export const metadata = {
  title: "EV App",
  description: "EV Forecasting and Range System",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="flex">
        <Sidebar />
        <main className="flex-1 p-6">{children}</main>
      </body>
    </html>
  );
}
