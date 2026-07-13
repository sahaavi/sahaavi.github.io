from tests.site_harness import HugoSiteTestCase


class BaselineSiteTests(HugoSiteTestCase):
    def test_existing_public_routes_render(self) -> None:
        for route in (
            "/",
            "/projects/",
            "/projects/maintenance-eye/",
            "/projects/govtintel/",
            "/posts/",
            "/search/",
            "/tags/",
            "/categories/",
        ):
            with self.subTest(route=route):
                self.page_html(route)

    def test_feeds_and_search_index_remain_generated(self) -> None:
        for relative_path in (
            "index.xml",
            "index.json",
            "posts/index.xml",
            "projects/index.xml",
            "tags/index.xml",
        ):
            with self.subTest(path=relative_path):
                self.assertTrue((self.output_dir / relative_path).is_file())

    def test_draft_projects_are_not_published(self) -> None:
        for route in (
            "/projects/pennymize-ai-powered-personal-finance/",
            "/projects/price-prediction-platform-on-aws/",
        ):
            with self.subTest(route=route):
                self.assertFalse(self.page_path(route).exists(), route)
