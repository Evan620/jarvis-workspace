import { siteConfig } from "@/config/site";
import { SiteHeader } from "@/components/site-header";
import { SiteFooter } from "@/components/site-footer";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

export default function AdminPage() {
  return (
    <div className="min-h-screen bg-slate-50">
      <SiteHeader />
      <main className="mx-auto w-full max-w-6xl px-6 py-10">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <p className="text-sm font-semibold uppercase tracking-wide text-emerald-600">
              Admin Panel
            </p>
            <h1 className="text-3xl font-semibold text-slate-900 md:text-4xl">
              Marketplace Operations
            </h1>
            <p className="text-sm text-slate-500">
              Monitor submissions, compliance workflows, and investor onboarding.
            </p>
          </div>
          <Button variant="outline">Export Quarterly Report</Button>
        </div>

        <section className="mt-8 grid gap-4 md:grid-cols-3">
          {siteConfig.admin.alerts.map((alert) => (
            <Card key={alert}>
              <CardHeader>
                <CardTitle className="text-base">Operational Alert</CardTitle>
              </CardHeader>
              <CardContent className="text-sm text-slate-600">{alert}</CardContent>
            </Card>
          ))}
        </section>

        <section className="mt-8">
          <Card>
            <CardHeader>
              <CardTitle>Pending Project Reviews</CardTitle>
              <p className="text-sm text-slate-500">
                Projects awaiting admin action.
              </p>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Project</TableHead>
                    <TableHead>Owner</TableHead>
                    <TableHead>Stage</TableHead>
                    <TableHead>Submitted</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Action</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {siteConfig.admin.pendingProjects.map((project) => (
                    <TableRow key={project.name}>
                      <TableCell className="font-medium text-slate-900">
                        {project.name}
                      </TableCell>
                      <TableCell>{project.owner}</TableCell>
                      <TableCell>{project.stage}</TableCell>
                      <TableCell>{project.submitted}</TableCell>
                      <TableCell>
                        <Badge variant="secondary">{project.status}</Badge>
                      </TableCell>
                      <TableCell>
                        <Button size="sm" variant="outline">
                          Review
                        </Button>
                      </TableCell>
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
