import { siteConfig } from "@/config/site";
import { SiteHeader } from "@/components/site-header";
import { SiteFooter } from "@/components/site-footer";
import { InvestmentPipelineChart } from "@/components/charts/investment-pipeline-chart";
import { KpiCard } from "@/components/kpi-card";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-slate-50">
      <SiteHeader />
      <main className="mx-auto w-full max-w-6xl px-6 py-10">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <p className="text-sm font-semibold uppercase tracking-wide text-emerald-600">
              Investor Dashboard
            </p>
            <h1 className="text-3xl font-semibold text-slate-900 md:text-4xl">
              Portfolio Intelligence
            </h1>
            <p className="text-sm text-slate-500">
              Track commitments, pipeline velocity, and impact performance.
            </p>
          </div>
          <Badge variant="secondary">Last synced 2 hours ago</Badge>
        </div>

        <section className="mt-8 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {siteConfig.dashboard.kpis.map((kpi) => (
            <KpiCard key={kpi.label} {...kpi} />
          ))}
        </section>

        <section className="mt-8 grid gap-6 lg:grid-cols-[2fr,1fr]">
          <Card>
            <CardHeader>
              <CardTitle>Pipeline Growth ($M)</CardTitle>
              <p className="text-sm text-slate-500">
                Active capital deployed across AFCEN projects.
              </p>
            </CardHeader>
            <CardContent>
              <InvestmentPipelineChart />
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Sector Allocation</CardTitle>
              <p className="text-sm text-slate-500">
                Current portfolio concentration.
              </p>
            </CardHeader>
            <CardContent className="space-y-4">
              {siteConfig.dashboard.allocations.map((item) => (
                <div key={item.label} className="flex items-center justify-between">
                  <p className="text-sm text-slate-600">{item.label}</p>
                  <p className="text-sm font-semibold text-slate-900">
                    {item.value}
                  </p>
                </div>
              ))}
            </CardContent>
          </Card>
        </section>

        <section className="mt-8">
          <Card>
            <CardHeader>
              <CardTitle>Active Deal Flow</CardTitle>
              <p className="text-sm text-slate-500">
                Latest projects progressing through diligence.
              </p>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Project</TableHead>
                    <TableHead>Stage</TableHead>
                    <TableHead>Target</TableHead>
                    <TableHead>Impact Priority</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {siteConfig.projects.map((project) => (
                    <TableRow key={project.id}>
                      <TableCell className="font-medium text-slate-900">
                        {project.name}
                      </TableCell>
                      <TableCell>{project.stage}</TableCell>
                      <TableCell>{project.fundingTarget}</TableCell>
                      <TableCell>{project.impact}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </section>
      </main>
      <SiteFooter />
    </div>
  );
}
