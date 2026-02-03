import Link from "next/link";

export function SiteFooter() {
  return (
    <footer className="border-t border-slate-200/70 bg-white">
      <div className="mx-auto flex w-full max-w-6xl flex-col items-start justify-between gap-6 px-6 py-8 md:flex-row md:items-center">
        <div>
          <p className="text-sm font-semibold text-slate-900">
            AFCEN Project Marketplace
          </p>
          <p className="text-sm text-slate-500">
            Connecting climate-smart agriculture with catalytic capital.
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-4 text-sm text-slate-500">
          <Link href="/" className="hover:text-emerald-600">
            Marketplace
          </Link>
          <Link href="/dashboard" className="hover:text-emerald-600">
            Investor Dashboard
          </Link>
          <Link href="/admin" className="hover:text-emerald-600">
            Admin Panel
          </Link>
        </div>
      </div>
    </footer>
  );
}
